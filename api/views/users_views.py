from users.models import CustomUser
from django.http import request, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.users_serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.exceptions import ValidationError
from api.utils import success_response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Automatically raises ValidationError if invalid

        user = serializer.save()
        return success_response(
            message="User Created Successfully",
            data={"user": serializer.data},  # Returning user details
            request=request,
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raises exception if invalid
        return success_response(
            message="Login successful",
            data=serializer.validated_data,
            request=request,
            status_code=status.HTTP_200_OK
        )


class CustomTokenRefreshView(TokenRefreshView):
    # permission_classes = [IsAuthenticated]
    
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

# add member ot trainer views
