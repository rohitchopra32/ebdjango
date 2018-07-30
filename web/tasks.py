from ebdjango.celery import app
from celery_progress.backend import ProgressRecorder
import time

@app.task(bind=True)
def demotask(self, x, y):
    progress_recorder = ProgressRecorder(self)
    print("Demo task")
    print(str(x+y))

    for i in range(1,10):
        self.update_state(state='PROGRESS',meta={'current': i, 'total': 10, 'status': "Ok"})
        time.sleep(1)
        progress_recorder.set_progress(i + 1, 10)
    return {'current': 10, 'total': 10, 'status': 'SUCCESS','result': 42}
