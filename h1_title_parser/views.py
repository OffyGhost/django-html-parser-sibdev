from django.shortcuts import render
from django.shortcuts import render_to_response
from h1_title_parser.models import UserTask


# Create your views here.
def index(request):
    tasks = UserTask.objects.all()
    return render_to_response('index.html', {'tasks': tasks})
