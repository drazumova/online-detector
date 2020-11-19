kubectl create -f service-postgres-configmap.yaml
kubectl create -f service-postgres-storage.yaml
kubectl create -f service-postgres-deployment.yaml 
kubectl create -f service-postgres-service.yaml

# kubectl get svc service-postgres
