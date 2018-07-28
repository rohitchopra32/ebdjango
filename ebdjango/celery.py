from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebdjango.settings')
app = Celery('ebdjango')

app.config_from_object('django.conf:settings', namespace="CELERY")
app.conf.broker_url = 'redis://testing.1sceuo.ng.0001.aps1.cache.amazonaws.com:6379/0'
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

