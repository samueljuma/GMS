from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.users_serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.permissions import IsAdminOrTrainer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken    

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Automatically raises ValidationError if invalid

        user = serializer.save()
        return Response(
            data={"user": serializer.data},  # Returning user details
            status=status.HTTP_201_CREATED,
        )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raises exception if invalid
        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK,
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

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated] This has been set globally in settings

    def post(self, request):
        refresh_token = request.headers.get("Refresh-Token")  # Extract token from headers

        if not refresh_token:
            raise ValidationError({"detail": "Refresh Token is required to logout"})

        try:
            # Validate and blacklist refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (InvalidToken, TokenError) as e:  # Catch both exceptions
            raise ValidationError({"detail":"Token has expired or is Invalid"} )

        return Response(
            {"detail": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT,
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
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
