from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.users_serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.utils.permissions import IsAdminOrTrainer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from datetime import datetime
from api.utils.filters import UserFilter
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )  # Automatically raises ValidationError if invalid

        user = serializer.save()
        return Response(
            data={
                "message": "Registration Successful - Awaiting Approval",
                "user": serializer.data,
            },
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

        response = Response(
            {"user": serializer.validated_data["user"]},
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
        refresh_token = request.COOKIES.get("Refresh")  # Extract from cookies

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
            raise ValidationError({"detail": "Token has expired or is Invalid"})

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
    search_fields = ["username", "first_name", "last_name"]
    ordering_fields = ["id", "username", "role", "dob"]
    ordering = ["id"]

    def get_queryset(self):
        """
        Admins see all users except other Admins.
        Trainers only see Members.
        """
        user = self.request.user  # Currently logged-in user

        if user.role == "Admin":
            return CustomUser.objects.all() # Admins see Trainers & Members
        elif user.role == "Trainer":
            return CustomUser.objects.filter(role="Member")  # Trainers see only Members
        return CustomUser.objects.none()  # Members should not see anyone
    
    def get_object(self):
        """
        Retrieve a user object while ensuring proper permission handling.
        This prevents "No user found" errors when the issue is actually permission-related.
        For retrieving user by ID Use Cases
        """
        # Fetch the user by ID without filtering the queryset
        user = self.request.user
        user_to_fetch = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        
        if user.role == "Member":
                raise PermissionDenied("You do not have permission to view this user.")
            
        if user.role == "Trainer" and user_to_fetch.role != "Member":
            raise PermissionDenied("You do not have permission to view this user.")

        # Let DRF handle object-level permission checks
        self.check_object_permissions(self.request, user_to_fetch)  

        return user_to_fetch


    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrTrainer])
    def approve(self, request, pk=None):
        """
        Custom action for Admins/Trainers to approve users.
        - Admins can approve both Trainers & Members.
        - Trainers can only approve Members.
        """
        user = request.user  # Approving user
        # Fetch the user directly, bypassing queryset filtering
        try:
            user_to_approve = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise NotFound("User does not exist.")

        # Check if user is already approved
        if user_to_approve.is_active:
            raise ValidationError("User is already approved")

        # Only Admins can approve Trainers
        if user_to_approve.role == "Trainer" and user.role != "Admin":
            raise PermissionDenied("Only Admins can approve Trainers")

        # Trainers can only approve Members
        if user.role == "Trainer" and user_to_approve.role != "Member":
            raise PermissionDenied("Trainers can only approve Members.")

        # Approve user
        user_to_approve.approved_by = user
        user_to_approve.is_active = True
        user_to_approve.save(update_fields=["approved_by", "is_active"])  # Update approved_by and is_active

        return Response(
            {
                "message": f"User {user_to_approve.username} approved successfully!",
                "user": UserSerializer(user_to_approve).data,
            },
            status=status.HTTP_200_OK,
        )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
