kubectl delete -f ${{ env.K8S_DIR }}/ ./k8s/common/
#kubectl delete service nginx1 || true
        
kubectl apply -f ${{ env.K8S_DIR }}/ ./k8s/common/
kubectl expose deployment nginx --name=nginx1 --type=LoadBalancer --port 80 --target-port 80
