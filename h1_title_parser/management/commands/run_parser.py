from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from h1_title_parser.models import UserTask, ReportTask
from threading import Thread
import re
import time
import urllib.request
import urllib.error
from django.utils import timezone

""" allows to use python2 and python3 """
try:
    from urllib.request import urlopen, URLError
    from queue import Queue
except ImportError:
    from urllib2 import urlopen, URLError
    from Queue import Queue


global_timeout = 1


class Command(BaseCommand):
    help = 'Запустить парсер отдельной командой'

    def handle(self, *args, **options):
        parser_queue = Queue()
        html_parser = Worker(parser_queue)
        thread = Thread(target=html_parser.run)
        thread.start()

        while True:
            # Запустить "не запушенные" задания и по времени
            now = timezone.now()
            task_pool = UserTask.objects.filter(status='0', date__lte=now)
            for task in task_pool:
                parser_queue.put(task)
            time.sleep(global_timeout)


class Worker:
    worker_have_task = True
    threads = []

    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.url_parse_timeout = global_timeout  # 5 seconds for timeout

    def process(self, task):
        print("Processing {}".format(task))
        task.status = 1
        task.save()

        thread = Thread(target=self.parse_url, args=(task,))
        thread.start()
        self.threads.append(thread)

        for tread in self.threads:
            tread.join()
            time.sleep(self.url_parse_timeout)

        html_status, encoding, h1, title = self.parse_url(task)
        # finally saving report
        save_user_task(task, html_status, encoding, h1, title)

    def run(self):
        while self.worker_have_task:
            try:
                task = self.work_queue.get()
                self.process(task)

            except ObjectDoesNotExist:
                self.worker_have_task = False
                print("Пул задач пуст")

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

        except urllib.error.HTTPError as error:
            html_status = error.code
            task.status = 2
            task.save()
        return html_status, encoding, h1, title


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
    task.save()
