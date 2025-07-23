from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('account', include(router.urls)),
    path("auth/google/", views.GoogleAuthAPIView.as_view(), name="google-login"),
    path('auth/google/client-id/', views.GoogleClientIDAPIView.as_view(), name='google-client-id'),
    path('home', views.home),
]