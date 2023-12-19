""" Serializers for Projects and SubProjects"""
from rest_framework import serializers
from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer"""
    class Meta:
        model = Project
        fields = ['id', 'title']
        read_only = ['id']


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for Project Detail view"""
    
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['description']