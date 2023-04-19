import random
import string
import os
import time
from typing import Optional

from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel, Field

# from google.cloud import storage

from api.tasks import long_running_task

API_KEY: str = os.environ["API_KEY"]

app = FastAPI()


def generate_uid(uid_len: Optional[int] = 12):
    uid: str = ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(uid_len)
    )

    return uid


def upload_to_gcs(bucket_name: str, file_name: str, data: bytes):
    # Implement your Google Cloud Storage upload logic here
    # Upload the data to the specified bucket with the given file name
    
    # Replace this with your actual GCS upload logic
    # client = storage.Client()
    # bucket = client.bucket(bucket_name)
    # blob = bucket.blob(file_name)
    # blob.upload_from_string(data)
    pass


def generate_download_url(bucket_name: str, file_name: str):
    # Implement your Google Cloud Storage download URL generation logic here
    # Generate a URL for downloading the file from the specified bucket
    
    # Replace this with your actual GCS download URL generation logic
    return f"https://storage.googleapis.com/{bucket_name}/{file_name}"


class TaskParams(BaseModel):
    start: str
    stop: str
    id: str
    api_key: str
    process_uid: str = Field(default=None)


@app.post("/process")
def process_data(params: TaskParams):
    # Compare the received api_key with the expected_api_key
    if params.api_key != API_KEY:
        return {"error": "Invalid API key"}
    
    if params.process_uid is None:
        # Generate a UID for the task
        uid = generate_uid()
    else:
        uid = params.process_uid
    
    # Create a Celery task and pass the parameters to it
    long_running_task.apply_async(
        args=(params.start, params.stop, params.id, params.api_key), task_id=uid
    )
    
    # Generate the URL for the second endpoint
    result_url = f"/status/{params.api_key}/{uid}"
    
    return {"url": result_url, "uid": uid}


@app.get("/status/{api_key}/{uid}")
def get_status(api_key: str, uid: str):
    # Compare the received api_key with the expected_api_key
    if api_key != API_KEY:
        return {"error": "Invalid API key"}    
    # Check if the task is completed
    task = AsyncResult(uid)
    if task.ready():
        # Task is completed, get the result and return the download link
        if task.result:
            # Upload the result to Google Cloud Storage
            # Replace with your actual GCS bucket details
            gcs_bucket_name = 'your_bucket_name'
            gcs_file_name = f'{uid}.zip'
            
            # Upload the file to GCS
            upload_to_gcs(gcs_bucket_name, gcs_file_name, task.result)
            
            # Generate the download link
            download_url = generate_download_url(gcs_bucket_name, gcs_file_name)
            
            return {"status": "completed", "download_url": download_url}
        else:
            return {"status": "failed"}
    else:
        # Task is still running, return the status
        return {"status": "running"}
