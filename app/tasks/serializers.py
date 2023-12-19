""" Serializers for Tasks and SubTasks"""
from rest_framework import serializers
from core.models import Task, SubTask

class TaskSerializer(serializers.ModelSerializer):
    """Task Serializer"""
    class Meta:
        model = Task
        fields = ['id', 'title']
        read_only = ['id']


class TaskDetailSerializer(TaskSerializer):
    """Serializer for Task Detail view"""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['note', 'project', 'sub_project']