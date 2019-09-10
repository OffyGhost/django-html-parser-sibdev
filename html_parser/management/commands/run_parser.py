import os
import time
import asyncio
import websockets
from queue import Queue
from django.utils import timezone
from django.core.management.base import BaseCommand
from html_parser.websocket import check_updates
from html_parser.worker import Worker
from html_parser.models import UserTask
from threading import Thread


def web(port):
    # worst method ever
    os.system('python manage.py runserver 0.0.0.0:{} --insecure'.format(port))


class Command(BaseCommand):
    help = 'Запустить парсер отдельной командой'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('port', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--port',
            action='store_true',
            dest='delete',
            help='Add port to run django app',
        )

    def handle(self, *args, **options):

        port = options['port'][0]

        parser_thread = Thread(target=web, args=(port,))

        # run websocket in second thread; able to set port via params
        start_server = websockets.serve(check_updates, "localhost", 9999)
        global_timeout = 2
        asyncio.get_event_loop().run_until_complete(start_server)
        Thread(target=asyncio.get_event_loop().run_forever).start()

        try:
            parser_thread.start()
            work_queue = Queue()
            html_parser = Worker(work_queue, global_timeout)
            html_parser.start()

            # Другим потоком накидываю задания в очередь
            while True:

                now = timezone.now()
                for task in UserTask.objects.filter(status='0', date__lte=now):
                    work_queue.put(task)

                time.sleep(global_timeout * 3)

        except KeyboardInterrupt:
            # hard close application
            os._exit(0)
