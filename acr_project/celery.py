import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acr_project.settings')  # Fixed project name

app = Celery('acr_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()