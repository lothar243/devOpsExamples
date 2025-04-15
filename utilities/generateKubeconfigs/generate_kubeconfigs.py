import subprocess
import os
import csv
import yaml
import base64
import time

OUTPUT_DIR = "kubeconfigs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_kubectl(cmd_args):
    return subprocess.run(["kubectl"] + cmd_args, check=True, capture_output=True, text=True)

def create_namespace(ns):
    run_kubectl(["create", "namespace", ns])

def apply_yaml(yaml_data, namespace):
    result = subprocess.run(["kubectl", "apply", "-n", namespace, "-f", "-"],
                            input=yaml_data, text=True, check=True, capture_output=True)
    return result

def create_token_secret(ns, sa):
    secret_name = f"{sa}-token"
    manifest = f"""
apiVersion: v1
kind: Secret
metadata:
  name: {secret_name}
  namespace: {ns}
  annotations:
    kubernetes.io/service-account.name: {sa}
type: kubernetes.io/service-account-token
"""
    apply_yaml(manifest, ns)
    
    # Wait until the token is populated
    print(f"  ⏳ Waiting for token to be ready for {sa}...")
    for i in range(10):
        result = run_kubectl([
            "get", "secret", secret_name, "-n", ns,
            "-o", "jsonpath={.data.token}"
        ]).stdout.strip()
        if result:
            return secret_name
        time.sleep(1)
    raise RuntimeError(f"Token not available for {sa} in namespace {ns}.")

def create_rbac(ns, user):
    manifest = f"""
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {user}
  namespace: {ns}
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: {user}-role
  namespace: {ns}
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "deployments", "replicasets"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: {user}-binding
  namespace: {ns}
subjects:
  - kind: ServiceAccount
    name: {user}
    namespace: {ns}
roleRef:
  kind: Role
  name: {user}-role
  apiGroup: rbac.authorization.k8s.io

"""
    apply_yaml(manifest, ns)

def get_sa_token(ns, secret_name):
    token = run_kubectl([
        "get", "secret", secret_name, "-n", ns,
        "-o", "jsonpath={.data.token}"
    ]).stdout.strip()

    ca_crt = run_kubectl([
        "get", "secret", secret_name, "-n", ns,
        "-o", "jsonpath={.data['ca\\.crt']}"
    ]).stdout.strip()

    return base64.b64decode(token).decode(), base64.b64decode(ca_crt).decode()


def build_kubeconfig(ns, sa, token, ca_crt):
    cluster_info = yaml.safe_load(run_kubectl(["config", "view", "-o", "json"]).stdout)
    cluster_name = cluster_info["clusters"][0]["name"]
    server = cluster_info["clusters"][0]["cluster"]["server"]

    config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [{
            "name": cluster_name,
            "cluster": {
                "certificate-authority-data": base64.b64encode(ca_crt.encode()).decode(),
                "server": server
            }
        }],
        "users": [{
            "name": sa,
            "user": {
                "token": token
            }
        }],
        "contexts": [{
            "name": f"{sa}-context",
            "context": {
                "cluster": cluster_name,
                "namespace": ns,
                "user": sa
            }
        }],
        "current-context": f"{sa}-context"
    }
    return config

def process_students(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = row["username"]
            print(f"Processing {student}...")
            try:
                create_namespace(student)
            except subprocess.CalledProcessError:
                print(f"Namespace {student} already exists.")

            create_rbac(student, student)
            secret_name = create_token_secret(student, student)
            token, ca_crt = get_sa_token(student, secret_name)
            kubeconfig = build_kubeconfig(student, student, token, ca_crt)

            config_path = os.path.join(OUTPUT_DIR, f"{student}.kubeconfig")
            with open(config_path, "w") as kf:
                yaml.safe_dump(kubeconfig, kf)

            print(f"  ✔ Kubeconfig created: {config_path}")

if __name__ == "__main__":
    process_students("students.csv")
