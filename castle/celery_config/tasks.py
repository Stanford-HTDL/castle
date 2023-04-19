__author__ = "Richard Correro (richard@richardcorrero.com)"

from typing import Any

from castle.backend.tasks import backend_task

from .celery import celery_app


@celery_app.task
def task(*args, **kwargs) -> Any:
    result: Any = backend_task(*args, **kwargs)
    return result
