from rest_framework import serializers
from .models import (
    Page, Business, Contact, Location, Hour, Social, Media, FAQ,
    Card, Connection, Subscriber, Label, SubscriberLabel
)

# ✅ Reusable base to auto-fill user from request
class UserOwnedSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)  # Prevent user from being changed
        return super().update(instance, validated_data)

# ✅ Page
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ['owner', 'subscribers', 'created_at']

# ✅ Business
class BusinessSerializer(UserOwnedSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = ['user']

class ContactSerializer(UserOwnedSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['user']

class LocationSerializer(UserOwnedSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['user']

class HourSerializer(UserOwnedSerializer):
    class Meta:
        model = Hour
        fields = '__all__'
        read_only_fields = ['user']

class SocialSerializer(UserOwnedSerializer):
    class Meta:
        model = Social
        fields = '__all__'
        read_only_fields = ['user']

class MediaSerializer(UserOwnedSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = ['user']

class FAQSerializer(UserOwnedSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ['user']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ['user']

class ConnectionSerializer(UserOwnedSerializer):
    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ['user']

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
        read_only = ['user']

class Label(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
        read_only = ['user']
