from rest_framework import serializers
from . import models

class CartSerialiser (serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['user', 'id', 'created_at', 'updated_at']
        read_only_fields = ['user', 'id', 'created_at', 'updated_at']

class CartItemSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id', 'course']
        read_only_fields = ['id']

        
    
