from django.urls import path

from .views import CommentRetrieveUpdateDestroyAPIView


app_name = "comments"

urlpatterns = [
    path("<uuid:uuid>/", CommentRetrieveUpdateDestroyAPIView.as_view(), name="comments_retrieve_update_destroy"),
]
