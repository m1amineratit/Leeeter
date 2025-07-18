from credits.models import CreditsTransaction
from .models import (
    Page, Business, Contact, Location, Hour, Social, Media, FAQ,
    Card, Connection, Label, SubscriberLabel, Subscriber
)
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    PageSerializer, BusinessSerializer, ContactSerializer, LocationSerializer, HourSerializer,
    SocialSerializer, MediaSerializer, FAQSerializer, CardSerializer,
    ConnectionSerializer
)
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from .tasks import send_email_task, broadcast_send_email_task


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
        pages = Page.objects.filter(owner=self.request.user)
        return Connection.objects.filter(subscribed_pages__in=pages)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def charge_user(user, amount, description):
    try:
        user.credit.spend_credits(amount)
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
def send_email_from_page(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    to_email = request.data.get('to_email')

    if not all([subject, message, to_email]):
        return Response({'error' : 'Missing fields'}, status=400)
    
    try:
        page = Page.objects.get(owner=request.user)
    except ObjectDoesNotExist:
        return Response({'error' : 'Page not found for this user'}, status=404)
    
    subscribers_user = page.subscribers.all()
    if not subscribers_user(email=to_email).exists():
        return Response({'email' : 'Recipient is not a subscriber of your page'}, status=403)
    
    charge_user(request.user, 10, 'Send Email to subscriber')

    send_email_task.delay(subject, message, to_email)

    return Response({"message": "Email is being sent. 10 credits deducted."})

@api_view(['POST'])
@permission_classes([[permissions.IsAuthenticated]])
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

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def broadcast_message(request):
    user = request.user
    page_id = request.data.get('page_id')
    subject = request.data.get('subject')
    content = request.data.get('content')

    if user.profile.credits < 200:
        return Response({'error' : 'Credits not enough'}, status=403)
    
    page = Page.objects.get(id=page_id, user=user)
    subscribers = Subscriber.objects.filter(page=page)

    for subscriber in subscribers:
        broadcast_send_email_task.delay(
            to_email=subscriber.email,
            subject=subject,
            content=content,
        )

    user.profile.credits -= 200
    user.profile.credits.save()
    
    return Response({"message": "Broadcast scheduled."})