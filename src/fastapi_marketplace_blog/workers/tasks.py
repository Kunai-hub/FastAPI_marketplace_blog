from celery import Celery
from src.fastapi_marketplace_blog.core.config import config
from smtplib import SMTP_SSL
from email.message import EmailMessage

broker_url = f"amqp://{config.RABBITMQ_USER}:{config.RABBITMQ_PASSWORD}@rabbitmq:{config.RABBITMQ_PORT}//"
celery = Celery(main="worker", broker=broker_url)


@celery.task
def send_mail(email: str, username: str):
    smtp_host = config.SMTP_HOST
    smtp_port = config.SMTP_PORT
    email_from = config.EMAIL_FROM
    email_password = config.EMAIL_PASSWORD
    message = EmailMessage()
    message["From"] = email_from
    message["To"] = email
    message["Subject"] = "Добро пожаловать"
    message.set_content(f"Привет, {username}! Спасибо за регистрацию!", charset="utf-8")
    try:
        with SMTP_SSL(host=smtp_host, port=smtp_port) as server:
            server.login(user=email_from, password=email_password)
            server.send_message(msg=message)
    except Exception as e:
        print(f"Failed to send email {e}")
