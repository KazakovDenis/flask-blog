#!/bin/bash
# The script to handle webhooks from the Docker hub

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
    echo "pulling docker image: ${IMAGE}:${NEXT_TAG}"
    docker pull $IMAGE:$NEXT_TAG
    docker stop blog
    # TODO: downtime
    docker run -d \
        --name blog \
        --restart always \
        -p 127.0.0.1:8000:8000 \
        -v /var/run/postgresql:/run/postgresql \
        -v $LOG_VOLUME:/www/log \
        -v $STATIC_VOLUME:/www/public/volume \
        $IMAGE:$NEXT_TAG

    # Clean up
    docker rmi $IMAGE:$PREV_TAG
else
    echo "The image is up to date"
fi
