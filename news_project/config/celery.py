import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("news_project")

app.conf.enable_utc = False
app.conf.update(timezone='Asia/Yerevan')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    worker_max_tasks_per_child=1,
    broker_pool_limit=None
)

app.conf.beat_schedule = {
    'news': {
        'task': 'apps.news.tasks.scrapy_task',
        'schedule': 60.0,
    }
}

app.autodiscover_tasks()
