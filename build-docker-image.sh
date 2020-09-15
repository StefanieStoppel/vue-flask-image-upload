#!/usr/bin/env bash
set -e

IMAGE_NAME="cvp-web-app:latest"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" # directory of this script

# Build docker image
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"