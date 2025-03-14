from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Show these fields in the list view
    list_display = ("username", "email", "role", "dob", "profile_picture_preview", "is_staff", "is_superuser", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    # Define the form layout when editing a user
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "dob", "profile_picture")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Define the form layout when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "dob", "profile_picture"),
        }),
    )

    search_fields = ("username", "email", "role")
    ordering = ("username",)

    # Display profile pictures in the admin panel list view
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="50" height="50" style="border-radius:50%;" />')
        return "No Image"

    profile_picture_preview.short_description = "Profile Picture"
