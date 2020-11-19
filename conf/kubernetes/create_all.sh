# minikube addons enable ingress

kubectl create -f fingerprint-deployment.yaml
kubectl create -f fingerprint-service.yaml

kubectl create -f service-deployment.yaml
kubectl create -f service-service.yaml

# kubectl create -f ingress-controller.yaml

# kubectl get pods  -o custom-columns=PodName:.metadata.name,PodUID:.metadata.uid
