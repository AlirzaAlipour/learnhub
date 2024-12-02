from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers, models, permissions as custom_permissions

class CartViewset (viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerialiser

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            session_key = self.get_or_create_session_key(self.request)
            serializer.save(session_key=session_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Cart.objects.filter(user=self.request.user)
        session_key = self.get_or_create_session_key(self.request)   # For anonymous users, return carts by session key
        return models.Cart.objects.filter(session_key=session_key)

    def get_or_create_session_key(self, request):
        if not request.session.session_key:  # If no session exists, create one
            request.session.create()
        return request.session.session_key



class CartItemViewset (viewsets.ModelViewSet):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    
    def get_queryset(self):
        cart_id = self.kwargs['cart_pk']  # 'cart_pk' is the default name for the lookup in NestedDefaultRouter
        return models.CartItem.objects.filter(cart__id=cart_id)
    
    def create(self, request, cart_pk=None):
        cart = models.Cart.objects.get(id=cart_pk)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(cart=cart) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderViewset (viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Order.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        return Response(serializer.data)
    

class OrderItemViewset (viewsets.ModelViewSet):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsOrderOwner]

    def get_permissions(self):
           if self.action in ['list', 'create']:
               return [permissions.IsAuthenticated(), custom_permissions.IsOrderOwner() ]
           return super().get_permissions()

    def get_queryset(self):
        order_id = self.kwargs['order_pk']
        order = models.Order.objects.get(id=order_id)
        self.check_object_permissions(self.request, order)
        return models.OrderItem.objects.filter(order_id= order_id)


    def create(self, request, *args, **kwargs):
        order_id = self.kwargs['order_pk']
        order = models.Order.objects.get(id=order_id)
        self.check_object_permissions(self.request, order) # DRF automatically calls check_object_permissions on the object being returned by the serializer but i use Order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer, order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, order):
        # Save the OrderItem with the associated Order
        serializer.save(order=order)

        
@api_view(['POST'])
def order_payment(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    order.status = 'completed'  # Assuming 'completed' is a valid status
    order.save()

    return Response({"message": "Payment processed successfully, order status updated to completed."}, 
                    status=status.HTTP_200_OK)
