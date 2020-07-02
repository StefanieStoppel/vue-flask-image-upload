#!/usr/bin/env bash

IMAGE_NAME="cvp-web-app:latest"

# cd into client and run yarn build
cd ./client || { echo "cd failed"; exit; }
yarn build
cd ..

# Build docker image
docker build -t "$IMAGE_NAME" .