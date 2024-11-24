from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers, models

class CartViewset (viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerialiser


class CartItemViewset (viewsets.ModelViewSet):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    
    def get_queryset(self):
        # Access the cart_id from the URL kwargs
        cart_id = self.kwargs['cart_pk']  # 'cart_pk' is the default name for the lookup in NestedDefaultRouter
        return models.CartItem.objects.filter(cart__id=cart_id)
    
    def create(self, request, cart_pk=None):
    # Retrieve the cart using cart_pk
        cart = models.Cart.objects.get(id=cart_pk)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Assign the cart instance to the serializer
            serializer.save(cart=cart)  # This line associates the cart with the CartItem
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
