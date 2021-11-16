from django.urls import path
from .views import (
    UserDetailsRetrieveUpdateAPIView,
    UserRetrieveAPIView,
    UserLikeAPIView,
    UserBookmarkAPIView,
    UserIncreaseShareAPIView,
)

app_name = "users"

urlpatterns = [
    # TODO: Add update users feature
    path("details/", UserDetailsRetrieveUpdateAPIView.as_view(), name="user_details_retrieve_update"),
    path("<uuid:uuid>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("<uuid:uuid>/like/", UserLikeAPIView.as_view(), name="user_like"),
    path("<uuid:uuid>/bookmark/", UserBookmarkAPIView.as_view(), name="user_bookmark"),
    path("<uuid:uuid>/share/", UserIncreaseShareAPIView.as_view(), name="user_increase_share"),
]
