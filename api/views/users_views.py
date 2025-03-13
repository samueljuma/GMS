from users.models import CustomUser
from django.http import request, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from api.serializers.users_serializers import UserRegistrartionSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrartionSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User Created Successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
