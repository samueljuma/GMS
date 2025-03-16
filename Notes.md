## Notes

- permissions are better places to restrict access than in views
- standrad responses for APIs are better handled by a renderer set globally in settings
- custom exeption handler alongside the renderer are greate for snadard error formats
- CustomUserManager alreday handles password hashing in its create functions. We just need to vall it when creating a user
- We can use Nested CustomSerializers for serializing objects within objects

```py
class AddedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "role"]

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model, using CustomUserManager for password handling."""

    password = serializers.CharField(write_only=True, required=False)
    added_by = AddedBySerializer(read_only = True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "role", "dob", "profile_picture", "password", "phone_number", "emergency_contact", "added_by"]
        extra_kwargs = {
            # "role": {"read_only": True},  # Prevent users from modifying their role
            "added_by": {"read_only": True}  # Prevents users from manually setting this field
        }

```
