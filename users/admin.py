from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Show these fields in the list view
    list_display = ("username", "email", "role", "dob", "profile_picture_preview", "phone_number", "emergency_contact", "self_registered", "approved_by", "added_by", "is_staff", "is_superuser", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "self_registered")

    # Define the form layout when editing a user
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "dob", "profile_picture", "phone_number", "emergency_contact")}),
        # ("Registration Details", {"fields": ("added_by", "approved_by")}), # Not needed - takes defaults
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Define the form layout when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email", "password1", "password2", "role", "dob", "profile_picture", "phone_number", "emergency_contact"),
        }),
    )

    search_fields = ("username", "email", "role")
    ordering = ("username",)

    # **Prefill `added_by` and `approved_by` with the current admin and self_registered to False.**
    def get_changeform_initial_data(self, request):
        return {
            "self_registered": False,
            "added_by": request.user,
            "approved_by": request.user,
        }

    # Auto-set `added_by` and `approved_by`
    def save_model(self, request, obj, form, change):
        obj.self_registered = False  # Always set to False
        if not obj.pk:  # If the user is being created
            obj.added_by = request.user  # Auto-set added_by to current admin
        if obj.self_registered is False and obj.approved_by is None:
            obj.approved_by = request.user  # Auto-set approved_by if not self-registered
        super().save_model(request, obj, form, change)

    # Display profile pictures in the admin panel list view
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="50" height="50" style="border-radius:50%;" />')
        return "No Image"

    profile_picture_preview.short_description = "Profile Picture"
