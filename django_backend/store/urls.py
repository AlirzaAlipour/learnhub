from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'carts', views.CartViewset)

carts_router = NestedDefaultRouter(router, r'carts', lookup='cart')
carts_router.register(r'cartitems', views.CartItemViewset, basename='cart-items')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(carts_router.urls)),
]