from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myaccountapp.settings')
app = Celery('myaccountapp')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
# app.conf.beat_schedule = {
#     'display_time-30-seconds': {
#         'task': 'bill.views.api_get_due_bills_view',
#     },
# }


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
