from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import models, serializers

class ProfileViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer




@api_view(["GET", "PATCH"])
def get_current(request):
    if not request.user.is_authenticated:
        return Response({'error': 'You must be logged in to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
    profile = get_object_or_404(models.User ,id = request.user.id)
    if request.method == 'GET':
        serializer = serializers.UserSerializer(profile)
        return Response(serializer.data)
    else:
        serializer = serializers.UserSerializer(profile ,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

