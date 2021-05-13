kubectl create -f fingerprint-postgres-configmap.yaml
kubectl create -f fingerprint-postgres-storage.yaml
kubectl create -f fingerprint-postgres-deployment.yaml 
kubectl create -f fingerprint-postgres-service.yaml

# kubectl get svc fingerprint-postgres
