from users.models import CustomUser
from django.http import request, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.users_serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Automatically raises ValidationError if invalid

        user = serializer.save()
        return Response(
            {
                "message": "User Created Successfully",
                "user": serializer.data,  # Returning user details
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raises exception if invalid
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.headers.get("Refresh-Token")  # Extract from headers

        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# add member ot trainer views
