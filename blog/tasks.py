import datetime
import environ

from django.core.mail import send_mail, BadHeaderError


from celery import shared_task
from celery.schedules import crontab

from .models import UserFollowing, User
from test_blog.celery import app


env = environ.Env()

environ.Env.read_env()


@app.task(serializer='json')
def get_total_followers_count():
    users = UserFollowing.objects.all()
    to_email = []
    followers = []
    for user in users:
        to_email.append(user.user_id.email)
        followers.append(user.following_user_id.email)

    amount_of_followers = len(followers)

    subject = f'Statistics of amount of yours followers'
    message = f'You have{amount_of_followers} followers'
    send_stats(subject, message, to_email)


@app.task(serializer='json')
def get_stats_subscription_by_day():

    to_email = []
    subscription_by_day = []
    today = str(datetime.datetime.today())[8:10]

    for user in User.objects.all():
        for u in UserFollowing.objects.all():
            if today == str(u.created)[8:10]:
                to_email.append(u.user_id.email)
                subscription_by_day.append(u.user_id.email)
        amount_of_subscription_by_day = len(subscription_by_day)
        subject = f'Statistics by previous day'
        message = f'You got a {amount_of_subscription_by_day} ' \
                  f'followers by previous day'
        send_stats(subject, message, user.email)


def send_stats(subject, message, to_email):
    send_mail(subject, message, env('EMAIL_LOGIN'),
                    to_email)