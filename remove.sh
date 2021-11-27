cont_id=`docker ps -a | grep "localhost:5000/python_api:1.0" | awk '{print $1}'`
docker kill "$cont_id"
docker rm "$cont_id"
for i in $(docker images | grep localhost:5000/python_api | awk '{print $3}'); do docker image rm $i; done
cont_id=`docker ps -a | grep "localhost:5000/nginx_app" | awk '{print $1}'`
docker kill "$cont_id"
docker rm "$cont_id"
for i in $(docker images | grep localhost:5000/nginx_app | awk '{print $3}'); do docker image rm $i; done