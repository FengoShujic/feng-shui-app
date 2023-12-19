"""Views for Tasks"""
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Task, SubTask
from tasks import serializers


class SubTaskViewSet(viewsets.ModelViewSet):
    """View for manage SubTask API"""
    serializer_class = serializers.SubTaskDetailSerializer
    queryset = SubTask.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive SubTask for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.SubTaskSerializer

        return self.serializer_class

    
    def perform_create(self, serializer):
        """Create new Task"""
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """View for manage Task API"""
    serializer_class = serializers.TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive Task for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class

    
    def perform_create(self, serializer):
        """Create new Task"""
        serializer.save(user=self.request.user)