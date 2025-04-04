from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
  list_display = ["member", "plan", "amount", "payment_method", "reference", "status", "created_at"]
  search_fields = ["member", "plan", "reference"]
  list_filter = ["status", "payment_method"]
