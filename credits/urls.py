from django.urls import path
from . import views

urlpatterns = [
    path('credits/add', views.add_credits),
    path('credits/balance', views.view_balance),
    path('credits/history', views.transaction_history),
    path('credits/use', views.use_credits),
]
