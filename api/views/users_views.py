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
from api.utils.permissions import IsAdminOrTrainer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken  
from datetime import datetime
from api.utils.filters import UserFilter

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


        # Get tokens from serializer
        tokens = {
            "access": serializer.validated_data["access"], 
            "refresh": serializer.validated_data["refresh"],
        }

        response =  Response(
            {
                "user": serializer.validated_data["user"]
            },
            status=status.HTTP_200_OK,
        )

        # Set HttpOnly cookies
        response.set_cookie(
            key="Authentication",
            value=tokens["access"],
            httponly=True,
            secure=True,  # Use True in production with HTTPS
            samesite="Lax",
            expires=datetime.fromisoformat(
                serializer.validated_data["access_expires_at"]
            ),
        )

        response.set_cookie(
            key="Refresh",
            value=tokens["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
            expires=datetime.fromisoformat(
                serializer.validated_data["refresh_expires_at"]
            ),
        )
        
        return response


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("Refresh") # Extract from cookies

        if not refresh_token:
            raise ValidationError("Refresh token is missing")

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        response = Response(
            {"detail": "Token Refresh Successful"},
            # serializer.validated_data, 
            status=status.HTTP_200_OK,
        )
        
        # Update Authentication cookie with new access token
        response.set_cookie(
            key="Authentication",
            value=serializer.validated_data["access"],
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated] This has been set globally in settings

    def post(self, request):
        refresh_token = request.COOKIES.get("Refresh")  # Extract from cookies

        if not refresh_token:
            raise ValidationError({"detail": "Refresh Token is required to logout"})

        try:
            # Validate and blacklist refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (InvalidToken, TokenError) as e:  # Catch both exceptions
            raise ValidationError({"detail":"Token has expired or is Invalid"} )

        response = Response(
            {"detail": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT,
        )

        # Clear cookies
        response.delete_cookie("Authentication")
        response.delete_cookie("Refresh")

        return response

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage Members and Trainers.
    - Admins can manage both Trainers and Members.
    - Trainers can manage only Members.
    """

    serializer_class = UserSerializer
    # authentication_classes = [JWTAuthentication] # Has been set globally to use Cookies 
    permission_classes = [IsAdminOrTrainer]
    
    filterset_class = UserFilter
    search_fields = ["username", "first_name", "last_name" ]
    ordering_fields = ["id", "username", "role", "dob"]
    ordering = ["id"]

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
