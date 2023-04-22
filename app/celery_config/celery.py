__author__ = "Richard Correro (richard@richardcorrero.com)"

from celery import Celery

import os

APP_BROKER_URI: str = os.environ["APP_BROKER_URI"]
APP_BACKEND_URI: str = os.environ["APP_BACKEND_URI"]

celery_app = Celery('celery_config',
             broker=APP_BROKER_URI,
             backend=APP_BACKEND_URI,
             include=['app.celery_config.tasks'])

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)


if __name__ == '__main__':
    celery_app.start()
