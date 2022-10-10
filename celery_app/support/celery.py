import os

from celery import Celery

app = Celery(
    'support',
    broker=f'amqp://{os.environ.get("RABBITMQ_DEFAULT_USER")}:{os.environ.get("RABBITMQ_DEFAULT_PASS")}@rabbit:5672',
    backend='rpc://',
    include=['support.tasks'],
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
