#!/bin/bash
# This script is for initial deployment only
# Docker & git should be installed
# Copy current directory and secrets to the server
# and run the script as a superuser:
# $ scp -r deploy/ .secrets user@host:
# $ ssh user@host
# $ sudo bash start_debian.sh
set -e

if [[ $UID -ne 0 ]]; then
  echo -e "Run the script as a superuser" && exit 1;
fi

# set env vars & aliases
sudo sh -c 'cat host.env | grep "^export" >> /etc/environment'
source /etc/environment

sudo sh -c 'cat host.env | grep "^alias" >> /etc/profile.d/aliases.sh'
source /etc/profile.d/aliases.sh

# create working dirs
sudo mkdir -p $DEPLOY_DIR $STATIC_REPO
sudo chown -R $USER $WORK_DIR
echo 1.0 > $DEPLOY_DIR/tag
mv ../.secrets $WORK_DIR
chmod +x run.sh
cp run.sh $DEPLOY_DIR
git init $STATIC_REPO
git -C $STATIC_REPO remote add origin $ORIGIN_REPO

# start project
source update.sh
rm $(ls)
