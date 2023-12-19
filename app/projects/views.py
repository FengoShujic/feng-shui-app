"""Views for Projects"""
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Project
from projects import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage Project API"""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive Projects for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')