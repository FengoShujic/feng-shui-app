"""Views for Projects"""
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Project, SubProject
from projects import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage Project API"""
    serializer_class = serializers.ProjectDetailSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive Projects for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.ProjectSerializer

        return self.serializer_class

    
    def perform_create(self, serializer):
        """Create new Project"""
        serializer.save(user=self.request.user)


class SubProjectViewSet(viewsets.ModelViewSet):
    """View for manage Project API"""
    serializer_class = serializers.SubProjectDetailsSerializer
    queryset = SubProject.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive SubProjects for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.SubProjectSerializer

        return self.serializer_class

    
    def perform_create(self, serializer):
        """Create new Project"""
        serializer.save(user=self.request.user)