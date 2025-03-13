from django.urls import path
from .views.users_views import sample_view

urlpatterns = [
    path("sample/",sample_view, name="sample" )
]
