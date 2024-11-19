from rest_framework import viewsets, permissions
from . import models, serializers, permissions as custom_permissions




class CourseViewset (viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    def get_permissions(self):

        if self.action == 'update':
            permission_classes = [custom_permissions.IsCourseOwnerOrReadOnly]
        elif self.action == 'destroy':
            permission_classes = [custom_permissions.IsCourseOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)



class ChapterViewset (viewsets.ModelViewSet):
    queryset = models.Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer
    permission_classes = [custom_permissions.IsChapterOwnerOrReadOnly]

    def perform_create(self, serializer):
        course_pk = self.kwargs['course_pk']
        course = models.Course.objects.get(pk=course_pk)
        serializer.save(course=course)

