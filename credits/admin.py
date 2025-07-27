from django.contrib import admin
from .models import CreditsTransaction, UserCredits

# Register your models here.

admin.site.register(UserCredits)
admin.site.register(CreditsTransaction)