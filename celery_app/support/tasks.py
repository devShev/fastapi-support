from celery.result import AsyncResult

from .celery import app


@app.task(name='celery_app.support.tasks.print_number')
def print_number(x, y) -> AsyncResult:
    return x * y
