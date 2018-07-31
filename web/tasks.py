from ebdjango.celery import app
from celery_progress.backend import ProgressRecorder
from django.core.mail import send_mail
from django.conf import settings
import time

@app.task(bind=True)
def demotask(self, x, y):
    progress_recorder = ProgressRecorder(self)
    print("Demo task")
    print(str(x+y))

    for i in range(1,10):
        if(i%30 == 0):
            process_percent = int(100 * float(i) / float(n))
            self.update_state(state='PROGRESS',
                                      meta={
                                      'process_percent': process_percent,
                                      'current': i, 
                                      'total': 10, 
                                      'status': "Ok"})
        # self.update_state(state='PROGRESS',meta={'current': i, 'total': 10, 'status': "Ok"})
        time.sleep(1)

        if settings.NOTIFY_EMAILS and settings.EMAIL_HOST_USER:
            send_mail(
                'Subject here',
                'Here is the message.',
                settings.EMAIL_HOST_USER,
                settings.NOTIFY_EMAILS,
                fail_silently=False,
            )
            progress_recorder.set_progress(i + 1, 10)
    return {'current': 10, 'total': 10, 'status': 'SUCCESS','result': 42}
