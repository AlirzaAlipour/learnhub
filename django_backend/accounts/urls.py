from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("profiles", views.ProfileViewset, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("me", views.get_current)
]
