from django.urls import path, include

urlpatterns = [
    # ...other routes...
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),  # Optional: for HTML, can be omitted for API-only
]