from django.urls import path, include
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# Create the main router
router = routers.SimpleRouter()
router.register(r'courses', views.CourseViewset)

# Create a nested router for chapters
courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'chapters', views.ChapterViewset, basename='course-chapters')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
]
