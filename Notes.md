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

# Secure JWT Authentication Using Cookies in Django

## Overview

When using JWT authentication with **access and refresh tokens in cookies**, it's crucial to configure security settings properly to prevent vulnerabilities like **CSRF (Cross-Site Request Forgery), XSS (Cross-Site Scripting), and token leakage**. This guide explains how to set up secure JWT authentication using Django and Django REST Framework (DRF).

---

## 1. Enable Secure Cookies (Prevent Token Theft)

Since tokens are stored in cookies, they should be:

- **`HttpOnly=True`** → Prevents JavaScript from accessing them (protects against XSS attacks).
- **`Secure=True`** → Ensures cookies are only sent over HTTPS (prevents MITM attacks).
- **`SameSite="Lax"` or `"Strict"`** → Helps prevent CSRF attacks.

```python
AUTH_COOKIE = "Authentication"  # Access Token Cookie Name
AUTH_COOKIE_REFRESH = "Refresh"  # Refresh Token Cookie Name
AUTH_COOKIE_DOMAIN = None  # Restrict to your domain if needed
AUTH_COOKIE_SECURE = True  # Send only over HTTPS
AUTH_COOKIE_HTTPONLY = True  # Prevent JavaScript access
AUTH_COOKIE_SAMESITE = "Lax"  # Prevent CSRF (use "Strict" if it's an SPA)
```

---

## 2. CSRF Protection

Even though **`SameSite="Lax"`** helps with CSRF, it's still a good idea to **require CSRF tokens for extra security**.

### Django Settings for CSRF

Modify `settings.py`:

```python
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SECURE = True  # Send only over HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access
CSRF_COOKIE_SAMESITE = "Lax"  # Or "Strict" for extra security
```

### Include CSRF Token in API Responses

Modify your login view to return a CSRF token in cookies:

```python
from django.middleware.csrf import get_token

class CustomLoginView(APIView):
    def post(self, request):
        # Authenticate user...
        response = Response({"message": "Login successful"})

        # Set CSRF token
        response.set_cookie(
            key="csrftoken",
            value=get_token(request),
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        return response
```

### Require CSRF Tokens in Requests

In **frontend requests**, send CSRF tokens in headers:

```js
fetch("/api/protected-route/", {
  method: "POST",
  credentials: "include",
  headers: {
    "X-CSRFToken": getCookie("csrftoken"), // Send CSRF token
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ data: "example" }),
});
```

---

## 3. Middleware Configuration

Ensure `CSRF` and `SessionAuthentication` middleware are enabled:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # Protects against CSRF
    "django.middleware.common.CommonMiddleware",
    "django.middleware.authentication.AuthenticationMiddleware",
]
```

---

## 4. Django REST Framework Settings

Modify `REST_FRAMEWORK` to use your custom authentication:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.CookieJWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # Needed for CSRF
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
```

---

## 5. Modify Your `CustomTokenRefreshView`

Your **`CustomTokenRefreshView`** must handle CSRF tokens correctly:

```python
from django.middleware.csrf import get_token

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("Refresh")

        if not refresh_token:
            raise ValidationError("Refresh token is missing")

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        response = Response(
            {"detail": "Token Refresh Successful"},
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

        # Set new CSRF token
        response.set_cookie(
            key="csrftoken",
            value=get_token(request),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response
```

---

## 6. Prevent Clickjacking

Add security headers in `settings.py`:

```python
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

## 7. Prevent Token Leaks in API Responses

Ensure tokens are never returned in API responses:

```python
class LoginView(APIView):
    def post(self, request):
        user = authenticate(...)
        if user:
            response = Response({"message": "Login successful"})  # ✅ No tokens in response
            response.set_cookie("Authentication", "ACCESS_TOKEN", httponly=True, secure=True)
            response.set_cookie("Refresh", "REFRESH_TOKEN", httponly=True, secure=True)
            return response
        return Response({"error": "Invalid credentials"}, status=400)
```

---

## 🔥 Final Checklist for Secure JWT in Cookies

- ✅ **Store tokens in HTTP-only, Secure cookies**
- ✅ **Use `SameSite="Lax"` or `"Strict"` to prevent CSRF**
- ✅ **Enable CSRF protection (`CSRF_COOKIE_HTTPONLY = True`)**
- ✅ **Send CSRF token in login and refresh responses**
- ✅ **Require CSRF tokens in API requests**
- ✅ **Enable `SessionAuthentication` middleware**
- ✅ **Prevent token leaks in API responses**
- ✅ **Block Clickjacking (`X_FRAME_OPTIONS = "DENY"`)**
- ✅ **Use HTTPS (Don't allow HTTP in production!)**

---


## Filtering, Searching and Ordering
- For FIltering, you need to install `django_filters` using `pip install django-filter` and include it installed apps 
```python
INSTALLED_APPS = [
    ...
    "django_filters",
]
```

- Ordering and searching are already supported in DRF - no installations required 
- Default filter backends can be set globally in `settings.py`
```py
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",  # Filtering
        "rest_framework.filters.SearchFilter",  # Searching
        "rest_framework.filters.OrderingFilter",  # Ordering
    ]
}
```

- Set up your views to use `filtering, ordering and searching`

```py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # Not needed since they've been set globally
    filterset_fields = ['title', 'author', 'publication_year']  # Enable filtering
    search_fields = ['title', 'author__name']  # Enable search
    ordering_fields = ['title', 'publication_year']  # Enable ordering
```

- `Filtering` is best for `exact matches` (e.g., ?role=Trainer&dob__gte=1990-01-01).
- `Searching` is best for `fuzzy text searches` (e.g., ?search=John).
- `Ordering` allows `sorting` of results (e.g., ?ordering=-dob to get youngest users first).

### Using nggrok to expose server to the internet. i.e testing for stkpush safaricom
- Expose Local Server to the Internet Using Ngrok - You need to sign up to ngrok to get auth-token
```bash
pip install pyngrok
ngrok config add-authtoken YOUR_AUTH_TOKEN 

python manage.py runserver
ngrok http 8000

Alternative to this is localtunnel
https://theboroer.github.io/localtunnel-www/

```
- Now use the public url
> Forwarding  https://random-id.ngrok.io -> http://127.0.0.1:8000


---
### Solving failed migrations
```bash 
$ python manage.py migrate --fake app_name zero

$ python manage.py makemigrations

$ python manage.py migrate app_name 0001


Alternatively
- Delete migrations ralated to the app from django-migrations table then run
python manage.py migrate payments zero --fake
python manage.py makemigrations payments
python manage.py migrate payments --fake-initial


```

### Solving Circular Imports 
> Instead of from payments.models import Payment, we use "payments.Payment" inside the OneToOneField. 
> This tells Django to resolve it later, avoiding the circular import issue.
```bash
 payment = models.OneToOneField("payments.Payment", on_delete=models.PROTECT, related_name="subscription_payment")  # Lazy reference
```
---
### Solving merge conflics using reset --hard
```bash
# Ensure Everything is Up to Date
git checkout payments
git pull origin payments
git checkout main
git pull origin main

# Overwrite main with payments
git checkout main
git reset --hard payments

# Push the Changes to Remote
git push origin main --force

```