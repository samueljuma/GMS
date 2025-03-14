from django.urls import path
from api.views.users_views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh Token
]
