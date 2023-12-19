""" Serializers for Projects and SubProjects"""
from rest_framework import serializers
from core.models import Project, SubProject


class SubProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProject
        fields = ['id', 'title']
        read_only_fields = ['id']

class SubProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta(SubProjectSerializer.Meta):
        fields = SubProjectSerializer.Meta.fields + ['description', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer"""
    class Meta:
        model = Project
        fields = ['id', 'title']
        read_only = ['id']


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for Project Detail view"""
    
    sub_projects = SubProjectDetailsSerializer(many=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['description', 'sub_projects']


