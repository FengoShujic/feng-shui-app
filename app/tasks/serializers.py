""" Serializers for Tasks and SubTasks"""
from rest_framework import serializers
from core.models import Task, SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    """Subtask Serializer"""
    class Meta:
        model = SubTask
        fields = ['id', 'title']
        read_only = ['id']


class SubTaskDetailSerializer(SubTaskSerializer):
    """Subtask Detail view"""
    class Meta(SubTaskSerializer.Meta):
        fields = SubTaskSerializer.Meta.fields + ['note', 'parent_task', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    """Task Serializer"""
    class Meta:
        model = Task
        fields = ['id', 'title']
        read_only = ['id']


class TaskDetailSerializer(TaskSerializer):
    sub_tasks = SubTaskDetailSerializer(many=True, read_only=True)

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['note', 'project', 'sub_project', 'created_at', 'updated_at', 'sub_tasks']
