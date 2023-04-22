#!/bin/bash

# Source the vars.env file to set environment variables
set -a
source vars.env
set +a

# Create a new subdirectory named "logs" in the current directory
mkdir -p $LOG_DIR

# Start Redis in the background
redis-server > "$LOG_DIR/redis.log" 2>&1 &

# Start RabbitMQ in the background
rabbitmq-server > "$LOG_DIR/rabbitmq.log" 2>&1 &

# Start Celery worker
celery -A castle.celery_config worker -l INFO > "$LOG_DIR/celery.log" 2>&1 &

# Start FastAPI app
uvicorn castle.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/uvicorn.log" 2>&1 &