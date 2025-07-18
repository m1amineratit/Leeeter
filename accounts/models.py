from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from core.models import Page
# Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='profiles', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        default_page = Page.objects.first()
        Profile.objects.create(user=instance, page=default_page)
    else:
        instance.profile.save()
