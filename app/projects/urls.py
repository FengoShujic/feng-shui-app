""" URL mappings for Project app"""

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('project', views.ProjectViewSet)
router.register('subproject', views.SubProjectViewSet)
app_name = 'projects'



urlpatterns = [
    path('', include(router.urls))

]