#!/bin/bash
# The script to restart app with a newer image
# Requires: sudo apt install jshon
set -e

echo ">>>>> Starting app update"
source /etc/environment
IMAGE=kazakovdu/blog
CURRENT_TAG=$DEPLOY_DIR/tag

echo ">>>>> Getting the latest image tag"
URL="https://hub.docker.com/v2/repositories/$IMAGE/tags/?ordering=last_updated"
PAYLOAD=$(curl -L --fail $URL)
NEXT_TAG=$(echo $PAYLOAD | jshon -e results -e 0 -e name -u)
PREV_TAG=$(cat $CURRENT_TAG)
echo ">>>>> Tags: previous - ${PREV_TAG}, latest - ${NEXT_TAG}"

if [[ $NEXT_TAG == $PREV_TAG ]]; then
    echo ">>>>> The app is up to date."
    exit 0
fi

echo ">>>>> Pulling the latest docker image: ${IMAGE}:${NEXT_TAG}"
docker pull $IMAGE:$NEXT_TAG

RUNNING=$(docker ps -a -q --filter name=blog)

if [[ $RUNNING ]]; then
    echo ">>>>> Removing the previous container..."
    docker stop blog
    docker rm blog
fi

echo ">>>>> Starting a new container..."
# "--rm" & "--restart always" conflict
.$DEPLOY_DIR/run.sh $NEXT_TAG

SUCCESS=$(docker ps --filter name=blog --filter status=running)

if [[ $SUCCESS ]]; then
    echo $NEXT_TAG > $CURRENT_TAG

    if [[ $PREV_TAG ]]; then
        echo ">>>>> Removing the previous image..."
        docker rmi $IMAGE:$PREV_TAG
    fi
    echo ">>>>> Update successful!"
    exit 0
else
    echo ">>>>> New container start failed."
    # TODO: notification
    docker stop blog
    docker rm blog

    if [[ $PREV_TAG ]]; then
      echo ">>>>> Restarting the previous container..."
      .$DEPLOY_DIR/run.sh $PREV_TAG
    fi

    echo ">>>>> Update failed!"
    exit 1
fi
