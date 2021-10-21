from django.urls import path, include
from .views import SendCode, Login

app_name = "auth"

urlpatterns = [
    path("users/send_code/", SendCode.as_view(), name="SendCode"),
    path("users/login/", Login.as_view(), name="Login"),
]
