from django.db import models
from django.utils import timezone
import datetime


class ReportTask(models.Model):
    date = models.DateTimeField(null=False, blank=False, verbose_name='Время запуска')
    html_status = models.CharField(null=True, max_length=4, blank=True)
    encoding = models.CharField(null=True, max_length=4, blank=True)
    title = models.TextField(null=True, blank=True)
    h1 = models.TextField(null=True, blank=True)

    def __str__(self):
        task = UserTask.objects.get(report=self)

        if self.encoding or self.title or self.h1:
            return "{} - {} {} {}".format(task.url, self.encoding, self.title, self.h1)
        else:
            return "{}".format(task.url)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Отчет по заданию"
        verbose_name_plural = "Отчеты по заданиям"


class UserTask(models.Model):
    task_status_enum = (
        ('0', 'Не запущено'),  ('1', 'Выполняется'), ('2', 'Завершено'), ('3', 'Завершено с ошибкой')
    )
    date = models.DateTimeField(null=True, blank=True, verbose_name='Указать время выполнения')
    time_shift = models.PositiveIntegerField(null=True, blank=True, verbose_name='Или добавить секунды')
    status = models.CharField(max_length=12, choices=task_status_enum, default='0')
    url = models.URLField(blank=False, verbose_name='Корневая ссылка задания', unique=True)
    report = models.ForeignKey(null=True, blank=True, to=ReportTask,
                               on_delete=models.CASCADE, verbose_name='Отчет по заданию')

    def __str__(self):
        time_for_report = self.date.__format__("%d.%m.%Y %H:%m:%S")
        return "<дата {} >: {}".format(time_for_report, self.url)
    # dd.mm.yyyy HH:mm:ss

    def save(self, *args, **kwargs):
        # Вместо валидации
        if self.date is None or self.date < timezone.now():
            self.date = timezone.now()
        if self.time_shift is not None:
            self.date = self.date + datetime.timedelta(seconds=self.time_shift)
            self.time_shift = None
        if self.report is None:
            report = ReportTask.objects.create(date=self.date)
            self.report = report
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользовательское задание"
        verbose_name_plural = "Пользовательские задания"

