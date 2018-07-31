from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from celery.result import AsyncResult
from web.tasks import demotask
import json
import traceback
# Create your views here.

# def progress_view(request):
#     # context = {}
#     # if request.POST:
#     print("in views")
#     result = demotask.delay(10, 10)
#     context ={'task_id': result.task_id}
#     print(context)
#     return render(request, 'display_progress.html', context=context)

def poll_state(request):
    """ A view to report the progress to the user """
    try:
        data = 'Fail'
        if request.is_ajax():
            if 'task_id' in request.POST.keys() and request.POST['task_id']:
                task_id = request.POST['task_id']
                task = AsyncResult(task_id)
                data = task.result or task.state
            else:
                data = 'No task_id in the request'
        else:
            data = 'This is not an ajax request'
        print(data, '---------------------->')
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    except Exception as e:
        traceback.print_exc()
        return render(request,"display_progress.html", context={})

def progress_view(request):
    print(request.GET, request.POST)
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data':data,
            'task_id':job_id,
        }
        return render(request,"show_t.html",context=context)
    else:
        print("in views")
        result = demotask.delay(10, 10)
        context ={'task_id': result.task_id}
        print(context)
        return render(request,"display_progress.html",context=context)