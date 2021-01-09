#!/bin/bash
# The script to handle webhooks from the Docker hub
echo ">>>>> Restarting the app container with a new image"

source /etc/environment
IMAGE=kazakovdu/blog

# Get the last tag
URL="https://hub.docker.com/v2/repositories/$IMAGE/tags/?ordering=last_updated"
PAYLOAD=$(curl -L --fail $URL)
NEXT_TAG=$(echo $PAYLOAD | jshon -e results -e 0 -e name -u)

# Save the last tag
PREV_TAG=$(cat $DEPLOY_DIR/tag)
echo $NEXT_TAG > $DEPLOY_DIR/tag

if [[ $NEXT_TAG != $PREV_TAG ]]; then
    # Restart the app with a new image
    echo ">>>>> Pulling the docker image: ${IMAGE}:${NEXT_TAG}"
    docker pull $IMAGE:$NEXT_TAG

    # TODO: downtime
    if [[ $(docker ps -a -q --filter name=blog) ]]; then
        echo ">>>>> Removing the previous container..."
        docker stop blog && docker rm blog
    fi

    echo ">>>>> Starting a new container..."
    # "--rm" & "--restart always" conflict
    docker run -d \
        --name blog \
        --restart always \
        -p 127.0.0.1:8000:8000 \
        -v /var/run/postgresql:/run/postgresql \
        -v $LOG_VOLUME:/www/log \
        -v $PUBLIC_VOLUME:/www/public/volume \
        $IMAGE:$NEXT_TAG

    if [[ $PREV_TAG ]]; then
        echo ">>>>> Removing the previous image..."
        docker rmi $IMAGE:$PREV_TAG
    fi

else
    echo ">>>>> The image is up to date."
fi
