from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserCredits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    balance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - Balance {self.balance}"

    def add_credits(self, amount):
        """ Adds the specified amount of credits to the user's balance. """
        if amount <= 0:
            raise ValidationError("Amount to add must be positive.")
        self.balance += amount
        self.save()

    def deduct_credits(self, amount):
        """ Deducts the specified amount of credits from the user's balance. """
        if amount <= 0:
            raise ValidationError("Amount to deduct must be positive.")
        
        # Ensure balance does not go negative
        if self.balance <= 0:
            raise ValidationError("The balance cannot be negative.")

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