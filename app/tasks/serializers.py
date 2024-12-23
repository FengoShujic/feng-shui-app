""" Serializers for Tasks and SubTasks"""
from rest_framework import serializers
from core.models import Task, SubTask, Tag, Comment
from django.contrib.contenttypes.models import ContentType


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'content_type', 'object_id']
        read_only_fields = ('id', 'user', 'created_at', 'content_type', 'object_id')
    
    def create(self, validated_data):
        """Override create method to link comment with the content object."""
        content_object = self.context.get('content_object')
        
        comment = Comment.objects.create(
            user=self.context['request'].user,
            text=validated_data['text'],
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.pk  
        )
        return comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only = ['id']


class SubTaskSerializer(serializers.ModelSerializer):
    """Subtask Serializer"""
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'tags', 'end_date']
        read_only = ['id']

    
    def _get_or_create_tags(self, tags, instance):
        """Getting or creating tags handler"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            instance.tags.add(tag_obj)


    def create(self, validated_data):
        """Create SubTask"""
        tags = validated_data.pop('tags', [])
        sub_task = SubTask.objects.create(**validated_data)
        self._get_or_create_tags(tags, sub_task)
        return sub_task

    def update(self, instance, validated_data):
        """Update SubTask"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class SubTaskDetailSerializer(SubTaskSerializer):
    """Subtask Detail view"""
    comments = CommentSerializer(many=True, read_only=True)
    class Meta(SubTaskSerializer.Meta):
        fields = SubTaskSerializer.Meta.fields + ['note', 'parent_task', 'created_at', 'updated_at', 'comments']


class TaskSerializer(serializers.ModelSerializer):
    """Task Serializer"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'project', 'sub_project', 'tags', 'position', 'end_date', 'urgent', 'important', 'is_completed']
        read_only = ['id', 'position'] 

    def _get_or_create_tags(self, tags, task):
        """Getting or creating tags handler"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            task.tags.add(tag_obj)

    def create(self, validated_data):
        """Create Task and set its position"""
        tags = validated_data.pop('tags', [])
        task_count = Task.objects.count()
        task = Task.objects.create(**validated_data, position=task_count + 1)
        self._get_or_create_tags(tags, task)
        return task

    def update(self, instance, validated_data):
        """Update Task"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TaskDetailSerializer(TaskSerializer):
    sub_tasks = SubTaskDetailSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['note', 'project', 'sub_project', 'created_at', 'updated_at', 'sub_tasks', 'comments']


class TaskPositionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating only task position"""
    class Meta:
        model = Task
        fields = ['position']


    
