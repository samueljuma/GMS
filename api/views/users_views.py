from users.models import CustomUser
from django.http import request, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.users_serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.exceptions import ValidationError
from api.utils import success_response
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from api.serializers.users_serializers import UserSerializer, UserRegistrationSerializer
from api.permissions import IsAdminOrTrainer
from rest_framework import serializers

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )  # Automatically raises ValidationError if invalid

        user = serializer.save()
        return success_response(
            message="User Created Successfully",
            data={"user": serializer.data},  # Returning user details
            request=request,
            status_code=status.HTTP_201_CREATED,
        )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raises exception if invalid
        return success_response(
            message="Login successful",
            data=serializer.validated_data,
            request=request,
            status_code=status.HTTP_200_OK,
        )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.headers.get("Refresh-Token")  # Extract from headers

        if not refresh_token:
            raise ValidationError("Refresh token is missing")

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Token Refresh successful",
            data=serializer.validated_data,
            request=request,
            status_code=status.HTTP_200_OK,
        )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage Members and Trainers.
    - Admins can manage both Trainers and Members.
    - Trainers can manage only Members.
    """

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrTrainer]

    def get_queryset(self):
        """
        Admins see all users except other Admins.
        Trainers only see Members.
        """
        user = self.request.user  # Currently logged-in user

        if user.role == "Admin":
            return CustomUser.objects.exclude(role="Admin")  # Admins see Trainers & Members
        elif user.role == "Trainer":
            return CustomUser.objects.filter(role="Member")  # Trainers see only Members
        return CustomUser.objects.none()  # Members should not see anyone

    def perform_create(self, serializer):
        """
        - Admins can create both Trainers and Members.
        - Trainers can only create Members.
        """
        role = serializer.validated_data.get("role", "Member")

        if self.request.user.role == "Trainer" and role != "Member":
            raise serializers.ValidationError(
                {"role": "Trainers can only create Members."}
            )

        serializer.save()
        

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
