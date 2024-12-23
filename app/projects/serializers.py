""" Serializers for Projects and SubProjects"""
from rest_framework import serializers
from core.models import Project, SubProject, Task
from tasks.serializers import TaskDetailSerializer




class SubProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProject
        fields = ['id', 'title']
        read_only_fields = ['id']

class SubProjectDetailSerializer(SubProjectSerializer):
    tasks = TaskDetailSerializer(many=True, read_only=True, source='task_set')

    class Meta(SubProjectSerializer.Meta):
        fields = SubProjectSerializer.Meta.fields + ['description', 'project', 'tasks']



class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer"""
    class Meta:
        model = Project
        fields = ['id', 'title']
        read_only = ['id']


from typing import List
from rest_framework import serializers

class ProjectDetailSerializer(ProjectSerializer):
    sub_projects = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['description', 'sub_projects', 'tasks']

    def get_sub_projects(self, obj):
        """Get all subprojects for the current project."""
        sub_projects = SubProject.objects.filter(project=obj)
        return SubProjectSerializer(sub_projects, many=True).data if sub_projects.exists() else []

    def get_tasks(self, obj) -> List[dict]:
        """Get all tasks for the current project."""
        tasks = Task.objects.filter(project=obj)
        return TaskDetailSerializer(tasks, many=True).data if tasks.exists() else []




