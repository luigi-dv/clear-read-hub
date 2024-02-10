#!/bin/sh

export $(id)
echo "default:x:$uid:0:user for openshift:/tmp:/bin/bash" >> /etc/passwd

set -e

echo "Starting Unicorn ..."
exec uvicorn 'main:app' \
    --host '0.0.0.0' \
    --port '8000' \
    --workers 4 \
    --log-level 'trace'