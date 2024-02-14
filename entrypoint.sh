#!/bin/sh

# Exit on error
set -e

# Define a log file
LOGFILE="/home/app/logfile.log"

# Redirect stderr to the log file
exec 2>$LOGFILE

# Define a cleanup function
cleanup() {
    echo "An error occurred. Check the log file for details."
}

# Register the cleanup function to be called on script exit
trap cleanup EXIT

# Openshift runs containers as a random uid for security reasons
# uid=$(id -u)
# echo "default:x:$uid:0:user for openshift:/tmp:/bin/bash" >> /etc/passwd

# Start Gunicorn
echo "Starting Unicorn with 4 workers on port 8000 ..."
exec uvicorn 'main:app' \
    --host '0.0.0.0' \
    --port '8000' \
    --workers 4 \
    --log-level 'trace'