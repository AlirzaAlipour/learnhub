from rest_framework import serializers
from . import models

class CartSerialiser (serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['user', 'session_key', 'id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at','user', 'session_key',]

class CartItemSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id', 'course']
        read_only_fields = ['id']

        
    
