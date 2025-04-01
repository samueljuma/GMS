from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
  list_display = ["member", "plan", "amount", "payment_method", "transaction_id", "status", "created_at"]
  search_fields = ["member", "plan", "transaction_id"]
  list_filter = ["status", "payment_method"]
