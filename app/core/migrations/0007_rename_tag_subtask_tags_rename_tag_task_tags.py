# Generated by Django 4.2.8 on 2023-12-20 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_subtask_tag_task_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subtask',
            old_name='tag',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='tag',
            new_name='tags',
        ),
    ]