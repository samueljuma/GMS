from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from datetime import datetime, timezone


class AddedBySerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "role"]
        
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model, using CustomUserManager for password handling."""

    password = serializers.CharField(write_only=True, required=False)
    added_by = AddedBySerializer(read_only = True)
    approved_by = AddedBySerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "role", "dob", "profile_picture", "password", "phone_number", "emergency_contact", "is_active", "self_registered", "added_by", "approved_by"]
        extra_kwargs = {
            # "role": {"read_only": True},  # Prevent users from modifying their role
            "added_by": {"read_only": True},  # Prevents users from manually setting this field
            "self_registered": {"read_only": True},
            "approved_by": {"read_only": True},  # Prevents users from manually setting this field
            
        }

    def create(self, validated_data):
        """Use CustomUserManager to handle user creation and password hashing."""
        request = self.context["request"]
        validated_data["self_registered"] = False # Automatically set to false
        validated_data["added_by"] = request.user  # Automatically sets the logged-in user as `added_by`
        validated_data["approved_by"] = request.user  # Automatically sets the logged-in user as `approved_by
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Allow users to update their info and hash password if changed."""
        password = validated_data.pop("password", None)  # Remove password from validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Update other fields

        if password:
            instance.set_password(password)  # Hash new password

        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "password", "role", "dob", "profile_picture", "phone_number", "emergency_contact", "self_registered"]
        extra_kwargs = {"role": {"required": False}}  # Role is optional

    def create(self, validated_data):
        validated_data["self_registered"] = True
        validated_data["added_by"] = None
        validated_data["approved_by"] = None
        validated_data["is_active"] = False  # User will be inactive until approval
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data["username_or_email"]
        password = data["password"]

        # Try finding user by email first, then username
        user = CustomUser.objects.filter(email=username_or_email).first()
        if not user:
            user = CustomUser.objects.filter(username=username_or_email).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        # Authenticate user using the retrieved username
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        access_expiry = datetime.fromtimestamp(access["exp"], timezone.utc).isoformat()
        refresh_expiry = datetime.fromtimestamp(refresh["exp"], timezone.utc).isoformat()

        return {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(access),
            "access_expires_at": access_expiry,
            "refresh_expires_at": refresh_expiry,
        }
