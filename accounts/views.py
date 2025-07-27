from rest_framework import viewsets
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from social_django.utils import psa
from rest_framework.views import APIView
from requests.exceptions import HTTPError
import requests
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework import status
from django.conf import settings

# Create your views here.

class GoogleClientIDAPIView(APIView):
    permission_classes = [AllowAny]
    """
    Returns the Google OAuth client ID (public info) to the frontend.
    """
    def get(self, request):
        return Response({"client_id": settings.GOOGLE_CLIENT_ID})

class GoogleAuthAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        id_token = request.data.get("access_token")  # actually ID token here
        if not id_token:
            return Response({"error": "Missing ID token"}, status=400)

        # Verify the ID token with Google
        response = requests.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token}
        )

        if response.status_code != 200:
            return Response({"error": "Invalid ID token"}, status=400)

        user_data = response.json()

        email = user_data.get("email")
        name = user_data.get("name")

        if not email:
            return Response({"error": "Email not found in token"}, status=400)

        # Create or get user
        User = get_user_model()
        user, _ = User.objects.get_or_create(email=email, defaults={"username": email, "first_name": name})
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "email": user.email,
                "name": user.first_name
            }
        })
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({'message' : 'authenticated and u are the best in the world', 'user': request.user})

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)