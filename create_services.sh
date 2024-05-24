kubectl delete -f ./k8s/
kubectl delete service nginx1

kubectl apply -f ./k8s/
kubectl expose deployment nginx --name=nginx1 --type=LoadBalancer --port 80 --target-port 80
