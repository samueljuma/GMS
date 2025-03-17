import django_filters
from users.models import CustomUser

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="iexact")  # Case-insensitive
    email = django_filters.CharFilter(field_name="email", lookup_expr="iexact")  # Case-insensitive

    class Meta:
        model = CustomUser
        fields = ["role", "username", "email", "dob"]
