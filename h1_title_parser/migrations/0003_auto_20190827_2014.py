# Generated by Django 2.1.3 on 2019-08-27 20:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('h1_title_parser', '0002_auto_20190827_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttask',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания отчета'),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='h1_title_parser.ReportTask', verbose_name='Отчет по заданию'),
        ),
    ]