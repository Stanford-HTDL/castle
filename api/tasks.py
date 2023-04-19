import time

from .celery import app


@app.task
def long_running_task(start: str, stop: str, id: str, api_key: str):
    # Implement your long-running task here
    # This function will be executed asynchronously by Celery
    # You can pass the task result to this function and it will be available as `task.result`
    
    # Replace this with your actual long-running task implementation
    time.sleep(5)
    result = "This is the result of the long-running task"
    
    return result