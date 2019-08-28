from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from h1_title_parser.models import UserTask, ReportTask
import threading


class Command(BaseCommand):
    help = 'Сброс парсера'

    def handle(self, *args, **options):
        UserTask.objects.all().update(status=0)
        #ReportTask.objects.all().delete()

