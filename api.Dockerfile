FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./requirements.txt /app/requirements.txt
COPY ./_api_keys.json /app/_api_keys.json

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app