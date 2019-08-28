from django.core.management.base import BaseCommand
from threading import Thread

import os


class Command(BaseCommand):
    help = 'Concurently'

    def handle(self, *args, **options):

        threads = []

        web = os.system('python manage.py runserver 0.0.0.0:80 --insecure')
        parser = os.system('python manage.py run_parser')
        thread = Thread(target=web)
        thread.start()
        threads.append(thread)
        thread2 = Thread(target=parser)
        thread2.start()
        threads.append(thread2)
        for thread in threads:
            thread.join()
