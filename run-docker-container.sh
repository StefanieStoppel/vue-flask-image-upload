#!/usr/bin/env bash

DEFAULT_HOST_MOUNT_DIR="$HOME/Desktop/CVP/pipeline"
HOST_MOUNT_DIR=${1:-$DEFAULT_HOST_MOUNT_DIR}
CONTAINER_MOUNT_DIR=/app/data

# Run docker container
docker run \
 --user "$(id -u)":"$(id -g)" \
 -e "UPLOAD_PATH=$CONTAINER_MOUNT_DIR" \
 -p 5000:5000 \
 -v "$HOST_MOUNT_DIR":"$CONTAINER_MOUNT_DIR" \
 -it --rm "cvp-web-app:latest"