# Generated by Django 4.2.13 on 2024-12-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_subtask_end_date_task_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='position',
            field=models.BigIntegerField(default=0),
        ),
    ]
