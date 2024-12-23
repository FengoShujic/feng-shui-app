""" URL mappings for Task app"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('task', views.TaskViewSet)
router.register('subtask', views.SubTaskViewSet)
router.register('tag', views.TagViewSet)


app_name = 'tasks'



urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<uuid:id>/comments/', views.CommentCreateAPIView.as_view(), name='task-comments'),
    path('subtasks/<uuid:id>/comments/', views.CommentCreateAPIView.as_view(), name='subtask-comments'),
    path('comments/<uuid:pk>/', views.CommentDetailAPIView.as_view(), name='comment-detail')

]