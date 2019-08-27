from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class ReportTask(models.Model):
    date = models.DateTimeField(blank=False, default=timezone.now, verbose_name='Время создания отчета')
    html_status = models.CharField(max_length=4)
    encoding = models.CharField(max_length=4)
    title = models.TextField()
    h1 = models.TextField()

    def __str__(self):
        if self.encoding or self.title or self.h1:
            return "foreignkey - {} {} {}".format((UserTask.object.get(self.id)).url, self.title, self.h1, self.encoding)
        else:
            return "foreignkey".format((UserTask.object.get(self.id)))

    class Meta:
        ordering = ["-date"]
        verbose_name = "Отчет по заданию"
        verbose_name_plural = "Отчеты по заданиям"


class UserTask(models.Model):
    task_status_enum = (
        ('0', 'Не запущено'),  ('1', 'Выполняется'), ('2', 'Завершено'), ('3', 'Завершено с ошибкой')
    )
    date = models.DateTimeField(blank=False, default=timezone.now, verbose_name='Время создания')
    time_shift = models.DateTimeField(blank=True, verbose_name='Смещение задания по времени')
    completed = models.BooleanField(blank=False, verbose_name='Завершено')
    status = models.CharField(max_length=12, choices=task_status_enum, default='0')
    url = models.URLField(blank=False, verbose_name='Корневая ссылка задания')
    report = models.ForeignKey(blank=True, to=ReportTask, on_delete=models.CASCADE, verbose_name='Отчет по заданию')

    def __str__(self):
        if self.time_shift:
            time_for_report = (self.date+self.time_shift).__format__("%d.%m.%Y %H:%m:%S")
        else:
            time_for_report = self.date.__format__("%d.%m.%Y %H:%m:%S")
        return "<дата {} >: {}".format(time_for_report, self.url)
    # dd.mm.yyyy HH:mm:ss

    class Meta:
        ordering = ["-date"]
        verbose_name = "Пользовательское задание"
        verbose_name_plural = "Пользовательские задания"

