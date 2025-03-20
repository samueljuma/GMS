from django.db import models
from users.models import CustomUser
from subscriptions.models import Subscription

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("Cash", "Cash"),
        ("M-Pesa", "M-Pesa"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Only for M-Pesa
    subscription = models.OneToOneField(Subscription, on_delete=models.PROTECT, null = True, blank=True, related_name="payment")
    recorded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="recorded_payments")  # Admin/Trainer
    confirmed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="confirmed_payments")  # Manual confirmation (if Cash)
    confirmation_timestamp = models.DateTimeField(null=True, blank=True)  # When was it confirmed?
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.member.username} ({self.status})"
