from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path
from .views import SendCode, Login, UserDetails, UserUpdate

app_name = "authentication"

urlpatterns = [
    path("users/send_code/", SendCode.as_view(), name="send_code"),
    path("users/login/", Login.as_view(), name="login"),
    path("users/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("users/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/details/", UserDetails.as_view(), name="user_details"),
    path("users/update/<uuid:uuid>/", UserUpdate.as_view(), name="user_update"),
]
