#!/bin/bash
# The script to run a docker container
set -e
set -u
source /etc/environment

IMAGE=kazakovdu/blog
TAG=$1

if [[ -z $1 ]]; then
    TAG=$(cat tag)
fi

# "--rm" & "--restart always" conflict
docker run -d \
    --name blog \
    --restart always \
    -p 127.0.0.1:8000:8000 \
    -v /var/run/postgresql:/run/postgresql \
    -v $WORK_DIR/.secrets:/www/.secrets \
    -v $LOG_VOLUME:/www/log \
    -v $PUBLIC_VOLUME:/www/public/volume \
    $IMAGE:$TAG
