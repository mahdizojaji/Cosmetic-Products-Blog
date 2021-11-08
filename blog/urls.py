from django.urls import path, include

from .views import (
    ArticleListCreateAPIView,
    ArticleRetrieveUpdateDestroyAPIView,
    ArticleLikeAPIView, 
    ArticleBookmarkAPIView, 
    ArticleIncreaseShareAPIView,
    ArticlePublishAPIView,
    ArticleCommentListCreateAPIView,
)


app_name = "blog"

urlpatterns = [
    path("articles/", ArticleListCreateAPIView.as_view(), name="articles_list_create"),
    path("articles/<uuid:uuid>/", ArticleRetrieveUpdateDestroyAPIView.as_view(), name="articles_retrieve_update_destroy"),
    path("articles/<uuid:uuid>/comments/", ArticleCommentListCreateAPIView.as_view(), name="comments_list_create"),
    path("articles/like/<uuid:uuid>/", ArticleLikeAPIView.as_view(), name="articles_like"),
    path("articles/bookmark/<uuid:uuid>/", ArticleBookmarkAPIView.as_view(), name="articles_bookmark"),
    path("articles/share/<uuid:uuid>/", ArticleIncreaseShareAPIView.as_view(), name="articles_increase_share"),
    path("articles/publish/<uuid:uuid>/", ArticlePublishAPIView.as_view(), name="articles_publish"),
]
