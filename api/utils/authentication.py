from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class to extract JWT token from cookies.
    """

    def authenticate(self, request):
        auth_cookie = request.COOKIES.get("Authentication")  # Extract token from cookies

        if not auth_cookie:
            return None  # No authentication

        try:
            validated_token = self.get_validated_token(auth_cookie)
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None  # Invalid token
