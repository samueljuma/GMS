from django.urls import path, include
from api.views.users_views import RegisterView, LoginView, CustomTokenRefreshView, LogoutView
from api.views.payments_views import MpesaSTKPushView, mpesa_callback
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from api.views.users_views import UserViewSet
from api.views.subscriptions_views import PlanViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"subscriptions/plans", PlanViewSet, basename="plan")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),  # Refresh Token
    path("", include(router.urls)), 
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("mpesa/stkpush/", MpesaSTKPushView.as_view(), name="mpesa_stkpush"),
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),
]