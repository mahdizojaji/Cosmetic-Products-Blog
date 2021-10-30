from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path
from .views import (
    SendCodeAPIView,
    LoginAPIView,
    UserDetailsAPIView,
    UserProfileAPIView,
    UserLikeAPIView,
    UserBookmarkAPIView,
    UserShareAPIView,
)

app_name = "authentication"

urlpatterns = [
    path("users/send_code/", SendCodeAPIView.as_view(), name="send_code"),
    path("users/login/", LoginAPIView.as_view(), name="login"),
    path("users/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("users/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/details/", UserDetailsAPIView.as_view(), name="user_details"),
    path("users/profile/<uuid:uuid>/", UserProfileAPIView.as_view(), name="user_profile"),
    path("users/profile/like/<uuid:uuid>/", UserLikeAPIView.as_view(), name="user_like"),
    path(
        "users/profile/bookmark/<uuid:uuid>/",
        UserBookmarkAPIView.as_view(),
        name="user_bookmark",
    ),
    path("users/profile/share/<uuid:uuid>/", UserShareAPIView.as_view(), name="user_share"),
]
