""" Serializers for Projects and SubProjects"""
from rest_framework import serializers
from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer"""
    class Meta:
        model = Project
        fields = ['id', 'title', 'description']
        read_only = ['id']
