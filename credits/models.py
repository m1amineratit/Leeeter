from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class UserCredits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - Balance {self.balance}"
    

    def add_credits(self, amount):
        self.balance += amount
        self.save()
    
    def deducate_credits(self, amount):
        if self.balance <= 0:
            raise ValidationError("The balance not be negative")
        
        if self.balance < amount:
            raise ValidationError('Not enough credits')
        
        self.balance -= amount
        self.save()


class CreditsTransaction(models.Model):
    ADD = 'ADD'
    DEDUCT = 'DEDUCT'

    CREDITS_CHOICES = (
        (ADD, 'Add Credits'),
        (DEDUCT, 'Deduct Credits'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=CREDITS_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} {self.amount}"