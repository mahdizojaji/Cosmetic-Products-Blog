from django.urls import path

from .views import (
    ArticleListCreateAPIView,
    ArticleRetrieveUpdateDestroyAPIView,
    ArticleLikeAPIView, 
    ArticleBookmarkAPIView, 
    ArticleIncreaseShareAPIView
)

app_name = "blog"

urlpatterns = [
    path("articles/", ArticleListCreateAPIView.as_view(), name="articles_list_create"),
    path("articles/<uuid:uuid>/", ArticleRetrieveUpdateDestroyAPIView.as_view(), name="articles_retrieve_update_destroy"),
    path("articles/like/<uuid:uuid>/", ArticleLikeAPIView.as_view(), name="articles_like"),
    path("articles/bookmark/<uuid:uuid>/", ArticleBookmarkAPIView.as_view(), name="articles_bookmark"),
    path("articles/share/<uuid:uuid>/", ArticleIncreaseShareAPIView.as_view(), name="articles_increase_share"),
]
