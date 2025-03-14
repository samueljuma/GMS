from rest_framework import serializers
from users.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["id","username","first_name","last_name", "email", "password", "role", "dob", "profile_picture"]
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

