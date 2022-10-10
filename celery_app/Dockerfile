FROM python:3.10.7

COPY requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

COPY . /app/

ENTRYPOINT celery -A support worker -l INFO
