from django.db import models
from users.models import CustomUser

class Plan(models.Model):
    PLAN_CHOICES = [
        ("daily", "Daily"),
        ("monthly", "Monthly"),
        ("custom", "Custom"),
    ]

    name = models.CharField(max_length=100, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()


class Subscription(models.Model): 
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Expired", "Expired"),
        ("Cancelled", "Cancelled"),
    ]
    subscription_id = models.CharField(max_length=20, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="plan_subscriptions")
    member = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="member_subscriptions")
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    payment_reference = models.CharField(max_length=16, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.plan.name} ({self.status})"
