#!/bin/sh

# Source the vars.env file to set environment variables
set -a
source vars.env
set +a

# Start Celery worker(s)
docker compose -f docker-compose.worker.yml up --detach --build

# Start Traefik
docker compose -f docker-compose.traefik.yml up --detach --build

# Start Uvicorn
docker compose -f docker-compose.api.yml up --detach --build