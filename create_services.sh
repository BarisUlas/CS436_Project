kubectl apply -f ./k8s/
kubectl expose deployment nginx --name=nginx1 --type=LoadBalancer --port 80 --target-port 80
