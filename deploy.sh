#!/bin/sh

network_name=restapi_flat-network

if [ -z $1 ]; then
  echo "Usage: $0 docker_image_name"
  exit 1
fi
image=$1

docker pull $image
if [ $? -ne 0 ]; then
  echo "docker pull $image failed"
  exit 1
fi

container_id_long=$(docker run -d $image)
if [ $? -ne 0 ]; then
  echo "docker run $image failed"
  exit 1
fi
container_id_short=$(echo $container_id_long | cut -c -12)
container_ip=$(docker exec $container_id_short ip a | grep 'inet ' | fgrep -v '127.0.0.1' | awk '{ print $2 }' | head -1 | awk -F '/' '{ print $1 }')

nc -zv $container_ip 3031
if [ $? -ne 0 ]; then
  sleep 3
  nc -zv $container_ip 3031
  if [ $? -ne 0 ]; then
    echo "port 3031 check failed"
    exit 1
  fi
fi

docker network connect --alias $container_id_short $network_name $container_id_short
curl http://localhost/container/switchover?dest=$container_id_short
curl http://localhost/
if [ $? -eq 0 ]; then
  echo
  echo "deploy succeeded"
fi
