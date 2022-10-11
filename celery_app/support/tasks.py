import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from .celery import app


@app.task(name='celery_app.support.tasks.send_status_to_mail')
def send_status_to_mail(email: str, status: str):
    msg = MIMEMultipart()
    msg['From'] = os.environ.get("EMAIL_HOST_USER")
    msg['To'] = email
    msg['Subject'] = 'Ticket status changed'
    message = f'Ticket status changed to "{status}"'
    msg.attach(MIMEText(message, 'plain'))

    with SMTP_SSL(os.environ.get("EMAIL_HOST"), int(os.environ.get("EMAIL_PORT"))) as smtp:
        smtp.login(msg['From'], os.environ.get("EMAIL_HOST_PASSWORD"))
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

    print(f'Mail send to {email}')
