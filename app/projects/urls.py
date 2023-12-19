""" URL mappings for Project app"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
app_name = 'projects'



urlpatterns = [
    path('', include(router.urls))

]