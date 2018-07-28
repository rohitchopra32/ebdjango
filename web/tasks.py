from ebdjango.celery import app
import time

@app.task(bind=True)
def demotask(self, x, y):
    print("Demo task")
    print(str(x+y))

    for i in range(1,10):
        self.update_state(state='PROGRESS',meta={'current': i, 'total': 10, 'status': "Ok"})
        time.sleep(1)
    return {'current': 10, 'total': 10, 'status': 'SUCCESS','result': 42}
