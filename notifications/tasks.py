from django.core.mail import send_mail, BadHeaderError


from celery import shared_task
from celery.schedules import crontab


from test_blog.celery import app


@app.task(serializer='json')
def send_notification(subject,
                      message, from_email, to_email):
    send_mail(subject, message, from_email,
                    [to_email, ])