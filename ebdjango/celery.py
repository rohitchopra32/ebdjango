from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebdjango.settings')
app = Celery('ebdjango')

app.config_from_object('django.conf:settings', namespace="CELERY")
app.conf.broker_url = 'Your Redis Cluster URL'
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

