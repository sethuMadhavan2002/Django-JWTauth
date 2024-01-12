from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth.settings")

app = Celery("auth")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-adv-email-task": {
        "task": "users.views.send_adv_email_task",
        "schedule": crontab(minute="*/1"),
    },
}
