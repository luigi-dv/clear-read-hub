#!/bin/sh

# Exit on error
set -e

case "${1:-api}" in
    api)
        echo "Starting the API with ${WEB_CONCURRENCY:-2} workers on port 8000 ..."
        exec uvicorn 'main:app' \
            --host '0.0.0.0' \
            --port '8000' \
            --workers "${WEB_CONCURRENCY:-2}" \
            --proxy-headers \
            --log-level "$(echo "${LOG_LEVEL:-info}" | tr '[:upper:]' '[:lower:]')"
        ;;
    worker)
        echo "Starting the document processing worker ..."
        exec python worker.py
        ;;
    *)
        exec "$@"
        ;;
esac
