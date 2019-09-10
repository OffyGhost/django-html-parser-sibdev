from html_parser.models import UserTask
from django.views.generic import TemplateView


class UserTaskListView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(UserTaskListView, self).get_context_data(**kwargs)
        context['tasks'] = UserTask.objects.order_by('-date')
        return context

    def post(self):
        pass
