from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trashradar.settings')
# Set the default Django settings module for the 'celery' program.
app = Celery('trashradar', include=['utils.tasks.common'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('trashradar.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
