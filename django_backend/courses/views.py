from rest_framework import viewsets
from . import models
from . import serializers



class CourseViewset (viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer



class ChapterViewset (viewsets.ModelViewSet):
    queryset = models.Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer
