from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProfileSerializer
from .models import Profile


# Create your views here.

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter



class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)