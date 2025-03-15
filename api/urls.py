from django.urls import path, include
from api.views.users_views import RegisterView, LoginView, CustomTokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from api.views.users_views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),  # Refresh Token
    path("", include(router.urls)), 
]
