from django.urls import path
from api.views.users_views import RegisterView


urlpatterns = [
    path("auth/register/",RegisterView.as_view(), name="register" )
]
