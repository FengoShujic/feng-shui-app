""" URL mappings for Task app"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('task', views.TaskViewSet)

app_name = 'tasks'



urlpatterns = [
    path('', include(router.urls))
    
    ]