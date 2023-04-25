__author__ = "Richard Correro (richard@richardcorrero.com)"

import os
from typing import Any, List

from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse

from celery_config.celery import celery_app
from .utils import generate_uid, get_api_keys

API_KEYS_PATH: str = os.environ["API_KEYS_PATH"]
APP_TITLE: str = os.environ["APP_TITLE"]
APP_DESCRIPTION: str = os.environ["APP_DESCRIPTION"]
APP_VERSION: str = os.environ["APP_VERSION"]

valid_api_keys: List[str] = get_api_keys(api_keys_path=API_KEYS_PATH)

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)

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


@app.get("/")
async def redirect():
    return RedirectResponse(url=f"/redoc", status_code=303)


@app.post("/process", dependencies=[Depends(api_key_auth)])
async def process_data(params: TaskParams) -> dict:    
    if params.process_uid is None:
        # Generate a UID for the task
        uid = generate_uid()
    else:
        uid = params.process_uid
    
    celery_app.send_task(name="backend_task", task_id=uid)
    # # Create a Celery task and pass the parameters to it
    # task.apply_async(
    #     kwargs=params.dict(), task_id=uid
    # )
    
    # Generate the URL for the second endpoint
    result_url = f"/status/{uid}"
    
    return {"url": result_url, "uid": uid}


@app.get("/status/{uid}", dependencies=[Depends(api_key_auth)])
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
