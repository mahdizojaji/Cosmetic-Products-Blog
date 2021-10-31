from django.urls import path
from .views import (
    UserDetailsAPIView,
    UserProfileAPIView,
    UserLikeAPIView,
    UserBookmarkAPIView,
    UserShareAPIView,
)


app_name = "users"

urlpatterns = [
    path("details/", UserDetailsAPIView.as_view(), name="user_details"),
    path("<uuid:uuid>/", UserProfileAPIView.as_view(), name="user_profile"),
    path("<uuid:uuid>/like/", UserLikeAPIView.as_view(), name="user_like"),
    path("<uuid:uuid>/bookmark/", UserBookmarkAPIView.as_view(), name="user_bookmark"),
    path("<uuid:uuid>/share/", UserShareAPIView.as_view(), name="user_share"),
]
