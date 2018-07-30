from django.shortcuts import render
from web.tasks import demotask
# Create your views here.

def progress_view(request):
    # context = {}
    # if request.POST:
    result = demotask.delay(10, 10)
    context ={'task_id': result.task_id}
    return render(request, 'display_progress.html', context=context)