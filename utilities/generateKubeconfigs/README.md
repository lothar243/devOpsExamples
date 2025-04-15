Create a students.csv file, with the following format:
username
student1
student2
student3

Run generate_kubeconfigs.py to creat the yaml files to do the following
 - Create a namespace
 - Create a serviceAccount, role, and rolebinding
 - Generate the kubeconfig scoped to that namespace
 - Save the kubeconfig toa  folder as <student>.kubeconfig