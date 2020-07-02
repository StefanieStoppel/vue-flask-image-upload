#!/usr/bin/env bash

UPLOAD_PATH="${1:-/Users/sstoppel/Desktop/vue-flask-image-upload}"

python server/app.py --upload_path "$UPLOAD_PATH"