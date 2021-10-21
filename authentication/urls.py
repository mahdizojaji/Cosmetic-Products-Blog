from django.urls import path, include
from .views import SendCode, Login

app_name = "auth"

urlpatterns = [
    path("send_code/", SendCode.as_view(), name="SendCode"),
    path("login/", Login.as_view(), name="Login"),
]
