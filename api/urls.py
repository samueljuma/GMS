from django.urls import path, include
from api.views.users_views import RegisterView, LoginView, CustomTokenRefreshView, LogoutView
from api.views.payments_views import MpesaSTKPushView, mpesa_callback, FetchMpesaTransactionView, FetchPaymentRecords
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from api.views.users_views import UserViewSet
from api.views.subscriptions_views import PlanViewSet, FetchSubscriptions
from api.views.attendance_views import MarkAttendanceView, FetchAttendance

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"subscriptions/plans", PlanViewSet, basename="plan")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),  # Refresh Token
    path("", include(router.urls)), 
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("payments/initiate-payment/", MpesaSTKPushView.as_view(), name="initiate_payments"),
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),
    path("mpesa/transactions/", FetchMpesaTransactionView.as_view(), name="fetch-mpesa-transactions"),
    path("subscriptions/", FetchSubscriptions.as_view(), name="subscriptions"),
    path("payments/fetch-records/", FetchPaymentRecords.as_view(), name="payment_records"),
    path("attendance/mark-member-attendance/", MarkAttendanceView.as_view(), name="member_attendance"),
    path("attendance/fetch-attendance/", FetchAttendance.as_view(), name="attendance-records")
    
]