from rest_framework import serializers
from . import models

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'date_of_birth', 'phone_number', 'bio', 'location']
        read_only_fields = ['email']
        ref_name = "CustomUserSerializer"
