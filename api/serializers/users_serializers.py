from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from datetime import datetime, timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "dob",
            "profile_picture",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "password", "role", "dob", "profile_picture",]
        extra_kwargs = {"role": {"required": False}}  # Role is optional

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role", "Member"),
            dob=validated_data.get("dob"),
            profile_picture=validated_data.get("profile_picture"),
        )
        return user


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
            "message": "Login Successful",
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(access),
            "access_expires_at": access_expiry,
            "refresh_expires_at": refresh_expiry,
        }
