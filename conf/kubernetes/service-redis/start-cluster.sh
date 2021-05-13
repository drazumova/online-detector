CLUSTER_NODES=($(kubectl get pods -l app=redis -o jsonpath='{range.items[*]}{.status.podIP} '))
CLUSTER_NODES=${CLUSTER_NODES[@]/%/:6379}
POD=$(kubectl get pods -l app=redis -o jsonpath='{range.items[]}{@.metadata.name}')
echo $POD $CLUSTER_NODES
kubectl exec $POD -- bash -c "echo yes | redis-cli --cluster create $CLUSTER_NODES --cluster-replicas 1"
