"""Views for Tasks"""
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
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

    """
    @action(detail=False, methods=['post'])
    def set_positions(self, request):
        with transaction.atomic():
            tasks_data = request.data.get('tasks', [])
            task_ids = [task['id'] for task in tasks_data]
            tasks = Task.objects.filter(id__in=task_ids)
            
            # Ažurirajte pozicije za sve taskove
            for task_data in tasks_data:
                task = tasks.get(id=task_data['id'])
                old_position = task.position
                new_position = task_data['position']
                
                # Pomaknite taskove unazad ili unapred zavisno od promene pozicije
                if old_position < new_position:
                    # Task se pomera unazad, taskovi između se pomjeraju napred
                    tasks.filter(position__gt=old_position, position__lte=new_position).update(position=F('position') - 1)
                else:
                    # Task se pomera napred, taskovi između se pomjeraju unazad
                    tasks.filter(position__lt=old_position, position__gte=new_position).update(position=F('position') + 1)
                
                # Postavite novu poziciju za premješteni task
                task.position = new_position
                task.save()
                
            return Response({'status': 'positions updated successfully'})
    """

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


class CommentCreateAPIView(APIView):
    """View to create a comment for either Task or SubTask."""
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id, format=None):
        # Determine whether we're dealing with a Task or SubTask based on the URL pattern
        if 'subtasks' in request.path:
            content_object = get_object_or_404(SubTask, id=id)
        else:
            content_object = get_object_or_404(Task, id=id)

        # Create a Comment instance
        serializer = self.serializer_class(data=request.data, context={
            'request': request,
            'content_object': content_object
        })

        if serializer.is_valid():
            # Save the comment and relate it to the Task or SubTask
            serializer.save(
                user=request.user,
                content_type=ContentType.objects.get_for_model(content_object),
                object_id=content_object.id
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)