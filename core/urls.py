from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'business', views.BusinessView, basename='business')
router.register(r'contacts', views.ContactView, basename='contact')
router.register(r'locations', views.LocationView, basename='location')
router.register(r'hours', views.HoursView, basename='hour')
router.register(r'socials', views.SocialView, basename='social')
router.register(r'media', views.MediaView, basename='media')
router.register(r'faqs', views.FAQView, basename='faq')
router.register(r'cards', views.CardView, basename='card')
router.register(r'clients', views.ClientView, basename='client')
router.register(r'connections', views.ConnectionView, basename='connection')
router.register(r'profile', views.ProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls))
]