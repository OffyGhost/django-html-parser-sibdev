import re
import socket
import urllib.error
import urllib.request
from threading import Thread


class Worker(Thread):
    '''
    Description coming soon
    '''

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
        print(f'Work on {task}')
        task.status = 1
        task.save()

        self.parse_url(task)

    def parse_url(self, task):
        try:
            title = ''
            h1 = ''
            encoding = ''
            html = urllib.request.urlopen(
                task.url, timeout=self.url_parse_timeout)

            html_status = html.status
            html = html.read().decode('utf-8', 'ignore')

            try:
                title = re.findall(r'<title>(.*?)</title>', html)[0]
            except IndexError:
                pass
            try:
                # Open h1 until it will be the words
                h1 = re.findall(r'<h1>(.*?)</h1>', html)[0]
                while (re.findall(r'<(.*)>(.*?)</(.*)>', h1)):
                    h1 = re.findall(r'<(.*)>(.*?)</(.*)>', h1)[0][1]

            except IndexError:
                pass

            try:
                meta = re.findall(r'<meta (.*?)>', html)
                for item in meta:
                    if (re.findall(r'charset=(.*)', item)):
                        encoding = re.findall(
                            r'charset=(.*)', item)[0].replace('"', '')

            except IndexError:
                pass

        except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError,
                socket.timeout, socket.error) as error:
            try:
                html_status = error.code
            except AttributeError:
                html_status = "Bad request"
                task.status = task.task_status_enum[3]  # Complete with error
            task.save()

        save_user_task(task, html_status, encoding, h1, title)


def save_user_task(task, html_status, encoding, h1, title):
    '''
    Сохранить результат парсинга
    :param task:
    :param html_status:
    :param encoding:
    :param h1:
    :param title:
    :return: ничего
    '''
    task.html_status = html_status
    task.encoding = encoding
    task.title = title
    task.h1 = h1

    if encoding or h1 or title:
        task.status = task.task_status_enum[2]  # Выполнено
    else:
        task.status = task.task_status_enum[3]  # Выполнено с ошибкой

    task.save()
