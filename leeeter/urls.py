from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from accounts.views import GoogleLogin

schema_view = get_schema_view(
    openapi.Info(
        title="Leeeter API",
        default_version='v1',
        description="API documentation for leeeter project"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/google/login/', GoogleLogin.as_view(), name='google_login'),
    path('api/', include('core.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('credits.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
