FROM python:3.10

COPY ./app /app

COPY ./requirements.txt /requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install -r /requirements.txt

COPY ./_gcs_creds.json /_gcs_creds.json

COPY ./lorem_ipsum.txt /lorem_ipsum.txt

CMD celery -A app.celery_config worker -l INFO
