import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roxy_sys.settings')

app = Celery('roxy_admin')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'archive-and-reset-every-year': {
        'task': 'roxy_admin/tasks.py',
        'schedule': crontab(minute=0, hour=0,day_of_month=1, month_of_year=3),
    },
}