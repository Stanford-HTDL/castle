__author__ = "Richard Correro (richard@richardcorrero.com)"

from celery import Celery

celery_app = Celery('celery_config',
             broker='pyamqp://localhost:5672',
             backend='redis://localhost:6379',
             include=['castle.celery_config.tasks'])

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)
# celery_app.conf.task_serializer = 'pickle'
# celery_app.conf.result_serializer = 'pickle'
# celery_app.conf.accept_content = [
#     'application/json', 'application/x-python-serialize'
# ]


if __name__ == '__main__':
    celery_app.start()
