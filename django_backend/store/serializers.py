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

        
    
class OrderSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','user', 'total_price', 'created_at', 'status']
        read_only_fields = ['id', 'user', 'total_price', 'created_at', 'status']



class OrderItemSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id','order', 'course', 'price_at_purchase']
        read_only_fields = ['id','order', 'price_at_purchase']
