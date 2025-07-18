from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserCredits

@receiver(post_save, sender=User)
def create_credits_account(sender, instance, created, **kwargs):
    if created:
        UserCredits.objects.create(user=instance)