# Generated by Django 2.1.3 on 2019-08-28 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('h1_title_parser', '0004_auto_20190827_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttask',
            name='encoding',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='reporttask',
            name='h1',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='reporttask',
            name='title',
            field=models.TextField(null=True),
        ),
    ]
