import datetime
from django.db import models
from django.utils import timezone


class UserTask(models.Model):
    task_status_enum = (
        ('0', 'Не запущено'),  ('1', 'Выполняется'), ('2',
                                                      'Завершено'), ('3', 'Завершено с ошибкой')
    )
    date = models.DateTimeField(
        null=True, blank=True, verbose_name='Указать время выполнения')
    time_shift = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Или добавить секунды')
    status = models.CharField(
        max_length=12, choices=task_status_enum, default=task_status_enum[0])
    url = models.URLField(
        blank=False, verbose_name='Корневая ссылка задания')
    html_status = models.CharField(null=True, max_length=4, blank=True)
    encoding = models.CharField(
        null=True, max_length=4, blank=True, default='')
    title = models.TextField(null=True, blank=True, default='')
    h1 = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return f"{self.url}"

    # invert models.CASCADE
    # dd.mm.yyyy HH:mm:ss
    def format_dashboard_top(self):
        time_for_report = self.date.__format__("%d.%m.%Y %H:%m:%S")
        return f"<дата {time_for_report}>: {self.url}"

    # dd.mm.yyyy HH:mm:ss
    def format_dashboard_bottom(self):

        if self.encoding or self.title or self.h1:
            return f"{self.url} - {self.encoding} {self.title} {self.h1}"
        else:
            return f"{self.url}"

    def save(self, *args, **kwargs):
        # Вместо валидации
        if self.date is None or self.date < timezone.now():
            self.date = timezone.now()
        if self.time_shift:
            self.date = self.date + datetime.timedelta(seconds=self.time_shift)
            self.time_shift = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользовательское задание"
        verbose_name_plural = "Пользовательские задания"
