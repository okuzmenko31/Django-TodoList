import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TodoList.settings')

app = Celery('TodoList')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send-mail-every-1-minute': {
#         'task': 'Todo.tasks.send_registration_mail',
#         'schedule': crontab(minute='*/1')
#     }
# }
