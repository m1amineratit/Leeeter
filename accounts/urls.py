from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('account/', include(router.urls))
]