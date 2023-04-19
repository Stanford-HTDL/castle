from celery import Celery

celery_app = Celery('api',
             broker='pyamqp://localhost:5672',
             backend='redis://localhost:6379',
             include=['api.tasks'])

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()