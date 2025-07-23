from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

MODE_CHOICE = [
    ('online', 'Online'),
    ('offline', 'Offline'),
    ('hybrid', 'Hybrid'),
]

CARD_TYPE_CHOICES = [
    ('dummy', 'Page Type Dummy'),
    ('personel', 'Personal'),
    ('brand', 'Brand'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('archived', 'Archived'),
]

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=100, choices=CARD_TYPE_CHOICES, verbose_name='Card Type')
    page_name = models.CharField(max_length=100, verbose_name="Page or Brand Name")
    page_url = models.SlugField(unique=True, verbose_name="Page URL (subdomain or slug)")
    accept_terms = models.BooleanField(default=False)
    receive_newsletter = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.page_name

class Page(TimeStampedModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='pages')
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='pages_profiles/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='pages_cover/', blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_pages', blank=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=150)
    subscriber_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('page', 'email')

    def __str__(self):
        return f"{self.email} on {self.page.name}"
    

class Business(models.Model):
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='businesses')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='contacts')
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='locations')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location_address = models.CharField(max_length=150)

class Hour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='hours')
    hour = models.TimeField()

class Social(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='socials')
    platform = models.CharField(max_length=150)
    url = models.URLField()

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='media')
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    images = models.ImageField(upload_to='gallery/', blank=True, null=True)

class FAQ(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=150)

class Label(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)


class SubscriberLabel(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name='connections')
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    active = models.CharField(max_length=100, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.label} - {self.page}"
