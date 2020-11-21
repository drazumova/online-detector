VERSION=$1
eval $(minikube docker-env)

APP_HOME="../../app"
docker build -t fingerprint:$VERSION --no-cache -f fingerprint_Dockerfile $APP_HOME
docker build -t service:$VERSION --no-cache -f service_Dockerfile $APP_HOME
