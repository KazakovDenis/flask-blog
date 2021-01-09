#!/bin/bash
# The script to update static files from Github
echo ">>>>> Pulling static files & templates..."

shopt -s expand_aliases
source /etc/environment
source /etc/profile.d/aliases.sh
pullstatic
