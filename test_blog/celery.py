import os


from celery import Celery
from celery.schedules import crontab

p = os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_blog.settings')


app = Celery('test_blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#celery beat tasks

app.conf.beat_schedule = {
    'send-stats-amount-of-followers-every-day': {
        'task': 'blog.tasks.get_total_followers_count',
        'schedule': crontab(0, 0, day_of_month='1-30')
    },
    'send-stats-amount-of-followers-by-day-every-day': {
        'task': 'blog.tasks.get_stats_subscription_by_day',
        'schedule': crontab(0, 0, day_of_month='1-30')
    }
}