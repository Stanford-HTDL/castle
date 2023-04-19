#!/bin/bash

# Stop Celery worker
pkill -f 'celery -A castle.celery_config worker'

# Stop FastAPI app
pkill -f 'uvicorn castle.api.main:fastapi_app'

# Stop RabbitMQ
rabbitmqctl stop

# Stop Redis
redis-cli shutdown
