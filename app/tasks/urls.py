""" URL mappings for Task app"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('task', views.TaskViewSet)
router.register('subtask', views.SubTaskViewSet)

app_name = 'tasks'



urlpatterns = [
    path('', include(router.urls))
    
    ]