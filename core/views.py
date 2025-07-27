from credits.models import CreditsTransaction
from .models import (
    Page, Business, Contact, Location, Hour, Social, Media, FAQ,
    Card, Connection, Label, SubscriberLabel, Subscriber, Post
)
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    PageSerializer, BusinessSerializer, ContactSerializer, LocationSerializer, HourSerializer,
    SocialSerializer, MediaSerializer, FAQSerializer, CardSerializer,
    ConnectionSerializer, PostSerializer
)
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from .tasks import send_email_task, broadcast_send_email_task
from rest_framework.views import APIView
import requests
from django.conf import settings
from rest_framework import status
from django.shortcuts import get_object_or_404

# Page ViewSet with subscribe/unsubscribe actions
class PageViewSet(ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show pages owned by the user or all pages (customize as needed)
        return Page.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        page = self.get_object()
        page.subscribers.add(request.user)
        return Response({'status': 'subscribed'})

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        page = self.get_object()
        page.subscribers.remove(request.user)
        return Response({'status': 'unsubscribed'})

class Post(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        page = Page.objects.get(owner=self.request.user)
        return Page.objects.filter(page=page)
        
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
class PageAssistantAPIView(APIView):
    def post(self, request, page_id):
        user_message = request.data.get('message', '')
        if not user_message:
            return Response({'error' : 'Message is reuired'}, status=status.HTTP_400_BAD_REQUEST)
        
        page = get_object_or_404(Page, id=page_id)
        posts_text = '\n'.join(post.content for post in page.posts.all()[:10])

        context = f"""
        You are analyzing a social media page with the following information:
        Title: "{page.name}"
        Description: {page.description}

        Recent Posts:
        {posts_text}

        Media:
        Profile Image URL: {page.profile_image.url if page.profile_image else 'No profile image'}
        Cover Image URL: {page.cover_image.url if page.cover_image else 'No cover image'}
        """

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization" : f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type" : "application/json"
        }
        data = {
            "model" : "mistralai/mistral-small-3.2-24b-instruct:free",
            "messages" : [
                {"role": "system", "content": "You are an assistant that helps summarize and answer questions about social media pages."},
                {"role": "user", "content": f"{context}\n\nUser question: {user_message}"}
            ],
            "max_tokens": 300,
            'temperature': 0.7,
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if "choices" not in result:
                return Response({"error": "OpenRouter did not return 'choices'. Full response:", "response": result}, status=500)
            reply = result["choices"][0]["message"]["content"]
            return Response({"reply": reply})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# All other ViewSets now require a page relation
class BusinessView(ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Business.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContactView(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LocationView(ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HoursView(ModelViewSet):
    serializer_class = HourSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Hour.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SocialView(ModelViewSet):
    serializer_class = SocialSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Social.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MediaView(ModelViewSet):
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Media.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FAQView(ModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return FAQ.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CardView(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConnectionView(ModelViewSet):
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return connections where the related page's owner is the current user
        return Connection.objects.filter(page__owner=self.request.user)

    def perform_create(self, serializer):
        page = serializer.validated_data.get('page')

        # Optional: Check the page belongs to the user
        if page and page.owner != self.request.user:
            raise PermissionDenied("You cannot create a connection for a page you do not own.")

        serializer.save(user=self.request.user)

def charge_user(user, amount, description):
    try:
        user_credits = user.credits.first()
        if not user_credits:
            return PermissionDenied('User does not have a credits account')
        user_credits.deduct_credits(amount)
        CreditsTransaction.objects.create(
            user=user,
            transaction_type='SPEND',
            amount=amount,
            description=description
        )
    except ValueError:
        raise PermissionDenied("Insufficient credits")

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_email_from_page(request, page_id):
    subject = request.data.get('subject')
    message = request.data.get('message')
    to_email = request.data.get('to_email')

    if not all([subject, message, to_email]):
        return Response({'error' : 'Missing fields'}, status=400)
    
    try:
        page = Page.objects.get(id=page_id, owner=request.user)
    except ObjectDoesNotExist:
        return Response({'error' : 'Page not found for this user'}, status=404)
    

    if not Subscriber.objects.filter(page=page, email=to_email).exists():
        return Response({'email' : 'Recipient is not a subscriber of your page'}, status=403)
    
    try:
        charge_user(request.user, 10, 'Send Email to subscriber')
    except PermissionDenied as e:
        return Response({'error' : str(e)}, status=403)
    
    send_email_task.delay(subject, message, to_email)

    return Response({"message": "Email is being sent. 10 credits deducted."})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_label_to_subscriber(request):
    user = request.user
    page_id = request.data.get('page_id')
    label_name = request.data.get('label')
    subscriber_id = request.data.get('subscriber_id')

    if user.profile.credits < 200:
        return Response({'error' : 'Credits not enough'}, status=403)
    
    page = Page.objects.get(id=page_id)
    label, _ = Label.objects.get_or_create(user=user, page=page, name=label_name)
    subscriber = Subscriber.objects.get(id=subscriber_id, page=page)

    SubscriberLabel.objects.create(label=label, subscriber=subscriber)
    
    return Response({"message": f"Label '{label_name}' added to subscriber."})


from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def broadcast_message(request):
    user = request.user
    page_id = request.data.get('page_id')
    subject = request.data.get('subject')
    content = request.data.get('content')

    if user.profile.credits < 200:
        return Response({'error': 'Credits not enough'}, status=403)

    try:
        page = Page.objects.get(id=page_id, owner=user)
    except Page.DoesNotExist:
        return Response({'error': 'Page not found or not owned by you'}, status=404)

    subscribers = Subscriber.objects.filter(page=page)

    for subscriber in subscribers:
        broadcast_send_email_task.delay(
            to_email=subscriber.email,
            subject=subject,
            content=content,
        )

    user.profile.credits -= 200
    user.profile.save()

    return Response({"message": "Broadcast scheduled."})
