from django.core.management.base import BaseCommand
from html_parser.models import UserTask


class Command(BaseCommand):
    help = 'Сброс парсера'

    def handle(self, *args, **options):
        UserTask.objects.all().update(status=0)
