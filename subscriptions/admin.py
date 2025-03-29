from django.contrib import admin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days")
    search_fields = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("member", "plan", "status", "start_date", "end_date")
    list_filter = ("status", "plan")
    search_fields = ("member__username", "plan__name")
