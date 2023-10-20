#! /bin/bash

set -eu

APP_NAME=${APP_NAME:-"app:app"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8080}
WORKERS=${WORKERS:-1}
UVICORN_WORKER=${UVICORN_WORKER:-"uvicorn.workers.UvicornWorker"}

gunicorn ${APP_NAME} \
    -b ${HOST}:${PORT} \
    -w ${WORKERS} \
    -k ${UVICORN_WORKER} \
    --capture-output \
    --reload
