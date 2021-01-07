#!/bin/bash
# This script is for initial deployment only
# Docker & git should be installed
# Copy current directory to the server
# & run the script as a superuser

# set env vars & aliases
cat host.env >> /etc/environment
source /etc/environment

# create working dirs
sudo mkdir -p $DEPLOY_DIR $STATIC_REPO
touch tag
cp dockerhub_webhook.sh static_webhook.sh tag $DEPLOY_DIR
git init $STATIC_REPO
git remote add origin $ORIGIN_REPO

# start project
source static_webhook.sh
source dockerhub_webhook.sh
