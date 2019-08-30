import re
import socket
import urllib.error
import urllib.request
from threading import Thread
from h1_title_parser.models import UserTask, ReportTask


class Worker(Thread):

    def __init__(self, work_queue, global_timeout):
        super().__init__()
        self.work_queue = work_queue
        self.url_parse_timeout = global_timeout

    def run(self):
        while True:
            try:
                task = self.work_queue.get()
                thread = Thread(target=self.in_process, args=(task,))
                thread.start()
            finally:
                self.work_queue.task_done()

    # mark task as 'in process' if its crashing after
    def in_process(self, task):
        print("Processing:  {}".format(task.format_dashboard()))
        task.status = 1
        task.save()
        self.parse_url(task)

    def parse_url(self, task):
        try:
            title = ''
            h1 = ''
            encoding = ''
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

    print("Completed with status {} : {}".format(task.status, task.format_dashboard()))

    task.save()
