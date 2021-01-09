#!/bin/bash
# This script is for initial deployment only
# Docker & git should be installed
# Copy current directory to the server
# & run the script as a superuser:
# sudo bash start_debian.sh

# set env vars & aliases
sudo sh -c 'cat host.env | grep "^export" >> /etc/environment'
source /etc/environment

sudo sh -c 'cat host.env | grep "^alias" >> /etc/profile.d/aliases.sh'
source /etc/profile.d/aliases.sh

# create working dirs
sudo mkdir -p $DEPLOY_DIR $STATIC_REPO
touch $DEPLOY_DIR/tag
cp host.env dockerhub_webhook.sh static_webhook.sh $DEPLOY_DIR
git init $STATIC_REPO
git -C $STATIC_REPO remote add origin $ORIGIN_REPO

# start project
source static_webhook.sh
source dockerhub_webhook.sh
