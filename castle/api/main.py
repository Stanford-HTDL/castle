__author__ = "Richard Correro (richard@richardcorrero.com)"

import os
from typing import Any, List

from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from castle.api.utils import get_api_keys
from castle.celery_config.celery import celery_app
from castle.celery_config.tasks import task
from castle.utils import generate_uid

API_KEYS_PATH: str = os.environ["API_KEYS_PATH"]
valid_api_keys: List[str] = get_api_keys(api_keys_path=API_KEYS_PATH)

fastapi_app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


class TaskParams(BaseModel):
    start: str
    stop: str
    id: str
    process_uid: str = Field(default_factory=generate_uid) # User may provide a process UID


@fastapi_app.post("/process", dependencies=[Depends(api_key_auth)])
async def process_data(params: TaskParams) -> dict:
    # # Compare the received api_key with the expected_api_key
    # validate_api_key(api_key=params.api_key, valid_api_keys=valid_api_keys)
    
    if params.process_uid is None:
        # Generate a UID for the task
        uid = generate_uid()
    else:
        uid = params.process_uid
    
    # Create a Celery task and pass the parameters to it
    task.apply_async(
        kwargs=params.dict(), task_id=uid
    )
    
    # Generate the URL for the second endpoint
    result_url = f"/status/{uid}"
    
    return {"url": result_url, "uid": uid}


@fastapi_app.get("/status/{uid}", dependencies=[Depends(api_key_auth)])
async def get_status(uid: str) -> dict:
    # # Compare the received api_key with the expected_api_key
    # validate_api_key(api_key=api_key, valid_api_keys=valid_api_keys)

    # Check if the task is completed
    task: AsyncResult = celery_app.AsyncResult(uid)
    if task.ready():
        # Task is completed, return the result(s)
        if task.successful():
            result: Any = task.result
            return {"status": "completed", "result": result}
        else:
            print(task.result)
            return {"status": "failed"}
    else:
        # Task is still running, return the status
        return {"status": "running"}
