#!/usr/bin/env bash

DEFAULT_DIR="$HOME/Desktop/test"
HOST_MOUNT_DIR=${1:-$DEFAULT_DIR}
CONTAINER_MOUNT_DIR=/app/data

# Run docker container
docker run \
 -e "UPLOAD_PATH=$CONTAINER_MOUNT_DIR" \
 -p 5000:5000 \
 -v "$HOST_MOUNT_DIR":"$CONTAINER_MOUNT_DIR" \
 -it "cvp-web-app:latest"