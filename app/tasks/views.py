"""Views for Tasks"""
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
# Create your views here.
from django.db.models import F
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Task, SubTask, Tag, Comment
from tasks import serializers
from rest_framework import status
from django.contrib.contenttypes.models import ContentType


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


class TagViewSet(mixins.DestroyModelMixin,
                mixins.UpdateModelMixin, 
                mixins.ListModelMixin, 
                viewsets.GenericViewSet):
    """Tags"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive Tag for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class CommentCreateAPIView(RetrieveAPIView):
    """View to create and retrieve comments for either Task or SubTask."""
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.kwargs.get('id')
        if 'subtasks' in self.request.path:
            return get_object_or_404(SubTask, id=id)
        else:
            return get_object_or_404(Task, id=id)

    def get(self, request, *args, **kwargs):
        content_object = self.get_object()
        serializer = self.serializer_class(content_object.comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        content_object = self.get_object()
        serializer = self.serializer_class(data=request.data, context={
            'request': request,
            'content_object': content_object
        })

        if serializer.is_valid():
            serializer.save(
                user=request.user,
                content_type=ContentType.objects.get_for_model(content_object),
                object_id=content_object.id
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
