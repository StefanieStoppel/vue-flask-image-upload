#!/usr/bin/env bash

IMAGE_NAME="cvp-web-app:latest"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" # directory of this script

# cd into client and run yarn build
cd "$SCRIPT_DIR"/client || { echo "cd failed"; exit; }
yarn build
cd ..

# Build docker image
docker build -t "$IMAGE_NAME" .