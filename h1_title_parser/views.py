from django.shortcuts import render_to_response
from h1_title_parser.models import UserTask, ReportTask


# Create your views here.
def index(request):
    tasks = UserTask.objects.all().order_by('-date')
    reports = ReportTask.objects.all().order_by('-date')
    return render_to_response('index.html', {'tasks': tasks, 'reports': reports})

