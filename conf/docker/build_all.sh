eval $(minikube docker-env)

APP_HOME="../../app"
docker build -t fingerprint -f fingerprint_Dockerfile $APP_HOME
docker build -t service -f service_Dockerfile $APP_HOME
