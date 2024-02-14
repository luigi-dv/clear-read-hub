#!/bin/sh

# Openshift runs containers as a random uid for security reasons
# uid=$(id -u)
# echo "default:x:$uid:0:user for openshift:/tmp:/bin/bash" >> /etc/passwd
# set -e

# Start Gunicorn
echo "Starting Unicorn ..."
exec uvicorn 'main:app' \
    --host '0.0.0.0' \
    --port '8000' \
    --workers 4 \
    --log-level 'trace'