import re
import os
import sys
import time
import socket
import urllib.request
import urllib.error
from queue import Queue
from django.utils import timezone
from threading import Thread
from django.core.management.base import BaseCommand
from h1_title_parser.models import UserTask, ReportTask


global_timeout = 2


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
        try:
            parser_thread.start()  # close this

            work_queue = Queue()
            html_parser = Worker(work_queue)
            html_parser.start()  # close this

            # Другим потоком накидываю задания в очередь
            while True:

                now = timezone.now()
                for task in UserTask.objects.filter(status='0', date__lte=now):
                    print('cant stop')
                    work_queue.put(task)

                time.sleep(global_timeout * 3)

        except KeyboardInterrupt:
            os._exit(0)


class Worker(Thread):

    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.url_parse_timeout = global_timeout

    def run(self):
        while True:
            try:
                task = self.work_queue.get()
                # Самая большая ошибка в том, что я не отслеживаю какой тред накрылся
                thread = Thread(target=self.process, args=(task,))
                thread.start()
            finally:
                self.work_queue.task_done()

    def process(self, task):
        print("Processing:  {}".format(task))
        task.status = 1
        task.save()
        self.parse_url(task)

    def parse_url(self, task):
        encoding = None
        h1 = None
        title = None

        try:
            html = urllib.request.urlopen(task.url, timeout=self.url_parse_timeout)
            html_status = html.status
            html = html.read().decode('utf-8', 'ignore')
            try:
                title = re.findall(r'<title>(.*?)</title>', html)[0]
            except IndexError:
                pass
            try:
                h1 = re.findall(r'<h1>(.*?)</h1>', html)[0]
            except IndexError:
                pass
            try:
                encoding = re.findall(r'<meta.*charset=(.*?)[" ]', html)[0]
            except IndexError:
                pass

        except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError,
                socket.timeout, socket.error) as error:
            try:
                html_status = error.code
            except AttributeError:
                html_status = "Bad request"
            task.status = 2
            task.save()

        save_user_task(task, html_status, encoding, h1, title)


def save_user_task(task, html_status, encoding, h1, title):

    user_task = UserTask.objects.filter(url=task.url)[0]
    if user_task.report is None:
        tmp = ReportTask.objects.create(html_status=html_status, encoding=encoding, h1=h1, title=title)
        task.report = tmp
    else:
        report = user_task.report
        ReportTask.objects.filter(id=report.id).update(html_status=html_status, encoding=encoding, h1=h1, title=title)

    if encoding or h1 or title:
        task.status = 2
    else:
        task.status = 3

    print("Completed with status {} : {}".format(task.status, task))

    task.save()
