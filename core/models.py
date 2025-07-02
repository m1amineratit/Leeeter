from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

MODE_CHOICE = [
    ('online', 'Online'),
    ('offline', 'Offline'),
    ('hybrid', 'Hybrid'),
]

class Page(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='pages_profiles/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='pages_cover/', blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_pages', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cleint_profiles')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='clients')
    full_name = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Business(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='businesses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=100, choices=MODE_CHOICE, verbose_name='Working Mode')
    activity = models.CharField(max_length=150, verbose_name='Business Activity')
    service = models.CharField(max_length=100, verbose_name='Service Offered')
    description = models.TextField(
        max_length=500,
        verbose_name='Short Description',
        help_text="Describe your business (500 character limit)."
    )
    expertise = TaggableManager()

    def __str__(self):
        return f"{self.activity} - {self.service}"

class Contact(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='contacts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()

class Location(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='locations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location_address = models.CharField(max_length=150)

class Hour(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='hours')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hour = models.TimeField()

class Social(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='socials')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instagram = models.CharField(max_length=150)
    facebook = models.CharField(max_length=150)
    snapshat = models.CharField(max_length=150)
    x = models.CharField(max_length=150)
    tikto = models.CharField(max_length=150)
    threads = models.CharField(max_length=150)
    linkedin = models.CharField(max_length=150)
    youtube = models.CharField(max_length=150)

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='media')
    cover_image = models.ImageField(upload_to='cover_images/')
    profile_image = models.ImageField(upload_to='profile/')
    video = models.FileField(upload_to='videos/')
    images = models.ImageField(upload_to='gallery/')

class FAQ(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=150)  # Fixed typo

class Card(models.Model):
    CARD_TYPE_CHOICES = [
        ('dummy', 'Page Type Dummy'),
        ('personel', 'Personel'),
        ('brand', 'Brand'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='cards')
    card_type = models.CharField(max_length=100, choices=CARD_TYPE_CHOICES, verbose_name='Card Type')
    page_name = models.CharField(max_length=100, verbose_name="Page or Brand Name")
    page_url = models.SlugField(unique=True, verbose_name="Page URL (subdomain or slug)")
    accept_terms = models.BooleanField(default=False)
    receive_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return self.page_name


class Connection(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_connections')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='connections')
    full_name = models.CharField(max_length=150)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='connection_locations')
    label = models.CharField(max_length=150)
    active = models.CharField(max_length=100, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.full_name

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='profiles')
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
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
