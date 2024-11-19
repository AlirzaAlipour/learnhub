from rest_framework import permissions
from . import models

class IsCourseOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.instructor == request.user
    

class IsChapterOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a `course` with an `instructor` attribute.
    """

    def has_permission(self, request, view):        # has_object_permission() is not called because there's no object to check permissions against yet.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For create action, check if user is the course instructor
        if view.action == 'create':
            course_pk = view.kwargs.get('course_pk')
            try:
                course = models.Course.objects.get(pk=course_pk)
                return course.instructor == request.user
            except models.Course.DoesNotExist:
                return False
        
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the course instructor
        return obj.course.instructor == request.user
