#!/bin/bash
# Docker entrypoint
set -e

if [ -e .secrets ]; then
  make init_app

  if [ -ne $@ ]; then
    make prod
  else
    exec "$@"
  fi

else
  echo ".secrets does not exist"
  exit 1
fi
