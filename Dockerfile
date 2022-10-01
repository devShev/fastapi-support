FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/
ENV PYTHONPATH /code/src

EXPOSE 8000
CMD ["uvicorn", "src.support.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]