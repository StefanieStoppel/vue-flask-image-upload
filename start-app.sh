#!/usr/bin/env bash

UPLOAD_PATH="${1:-/Users/sstoppel/Desktop/vue-flask-image-upload}"

# cd into client and run yarn build
cd ./client || { echo "cd failed"; exit; }
yarn build
cd ..

python server/app.py --upload_path "$UPLOAD_PATH"