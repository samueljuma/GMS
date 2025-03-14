from users.models import CustomUser
from django.http import request, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.users_serializers import UserRegistrationSerializer


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