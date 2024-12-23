"""Views for Tasks"""
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.
from django.db.models import F
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
from tasks.serializers import TaskPositionUpdateSerializer
from django.core.exceptions import ValidationError


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
    """View for managing Task API"""
    serializer_class = serializers.TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Task for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-position')

    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'update_position':
            return TaskPositionUpdateSerializer
        if self.action == 'list':
            return serializers.TaskSerializer
        return self.serializer_class

    @action(detail=True, methods=['patch'], url_path='update_position')
    def update_position(self, request, pk=None):
        """Update Task position only"""
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Create new Task with automatic position"""
        task_count = Task.objects.count()  
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Delete Task and adjust positions of other tasks"""
        position = instance.position
        instance.delete()

        Task.objects.filter(position__gt=position).update(position=F('position') - 1)

    def perform_update(self, serializer):
        """Update Task position and adjust other tasks accordingly"""
        task = serializer.instance
        old_position = task.position
        new_position = serializer.validated_data['position']
    
        max_position = Task.objects.filter(user=self.request.user).count()
    
        if new_position < 1 or new_position > max_position:
            raise ValidationError(f"Invalid position! Select in range between 1 and {max_position}.")
    
        if old_position != new_position:
            if new_position < old_position:
                Task.objects.filter(position__gte=new_position, \
                    position__lt=old_position).update(position=F('position') + 1)
            else:
                Task.objects.filter(position__gt=old_position, \
                    position__lte=new_position).update(position=F('position') - 1)

            task.position = new_position
            task.save()
        else:
            super().perform_update(serializer)
        

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


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a comment."""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    # Token 42c2f3e6ea4bbb7c2dfeefdb55ba73173f6fd966