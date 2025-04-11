# Get the token for the ServiceAccount
export SECRET=$(kubectl -n rbac-demo get sa pod-reader -o jsonpath="{.secrets[0].name}")
export TOKEN=$(kubectl -n rbac-demo get secret $SECRET -o jsonpath="{.data.token}" | base64 --decode)

# Try listing pods using impersonation
kubectl get pods -n rbac-demo \
  --as=system:serviceaccount:rbac-demo:pod-reader \
  --token="$TOKEN" \
  --server=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}') \
  --insecure-skip-tls-verify
