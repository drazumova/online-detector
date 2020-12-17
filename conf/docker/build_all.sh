VERSION=$1
eval $(minikube docker-env)

APP_HOME="../../app"
docker build -t fingerprint:$VERSION -f fingerprint_Dockerfile $APP_HOME
docker build -t data_saver:$VERSION -f data_saver_Dockerfile $APP_HOME
docker build -t geoip:$VERSION -f geoip_Dockerfile $APP_HOME
docker build -t service:$VERSION -f service_Dockerfile $APP_HOME
