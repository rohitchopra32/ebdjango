from ebdjango.celery import app
from celery import shared_task, current_task
from celery_progress.backend import ProgressRecorder
from django.core.mail import send_mail
from django.conf import settings
import time
from numpy import random
from scipy.fftpack import fft


@shared_task
def fft_random(n):
    """
    Brainless number crunching just to have a substantial task:
    """
    for i in range(n):
        x = random.normal(0, 0.1, 2000)
        y = fft(x)
        if(i%30 == 0):
            process_percent = int(100 * float(i) / float(n))
            current_task.update_state(state='PROGRESS',
                                      meta={'process_percent': process_percent})
    return random.random()

@app.task(bind=True)
def demotask(self, x, y):
    progress_recorder = ProgressRecorder(self)
    print("Demo task")
    print(str(x+y))

    for i in range(1,10000):
        print(i%30, str(i)+'%30')
        if(i%30 == 0):
            
            process_percent = int(100 * float(i) / float(10000))
            current_task.update_state(state='PROGRESS',
                                      meta={
                                      'process_percent': process_percent,
                                       })
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
            #progress_recorder.set_progress(i + 1, 10)
    return {'current': 10, 'total': 10, 'status': 'SUCCESS','result': 42}
