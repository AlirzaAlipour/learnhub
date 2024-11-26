from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'carts', views.CartViewset)
router.register(r'orders', views.OrderViewset)

carts_router = NestedDefaultRouter(router, r'carts', lookup='cart')
carts_router.register(r'cartitems', views.CartItemViewset, basename='cart-items')

orders_router = NestedDefaultRouter(router, r'orders', lookup='order')
orders_router.register(r'orderitems', views.OrderItemViewset, basename='order-items')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(carts_router.urls)),
    path(r'', include(orders_router.urls)),
]