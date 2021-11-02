from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path
from .views import SendCodeAPIView, LoginAPIView


app_name = "authentication"

urlpatterns = [
    path("send_code/", SendCodeAPIView.as_view(), name="send_code"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
