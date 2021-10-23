from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path, include
from .views import SendCode, Login

app_name = "auth"

urlpatterns = [
    path("users/send_code/", SendCode.as_view(), name="send_code"),
    path("users/login/", Login.as_view(), name="login"),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
