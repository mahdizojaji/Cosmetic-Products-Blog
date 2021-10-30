from django.urls import path

from .views import (
    ArticleListAPIView, 
    ArticleDetailsAPIView, 
    ArticleLikeAPIView, 
    ArticleBookmarkAPIView, 
    ArticleShareAPIView
)

app_name = "blog"

urlpatterns = [
    path("articles/", ArticleListAPIView.as_view(), name="articles_list"),
    path("articles/<uuid:uuid>/", ArticleDetailsAPIView.as_view(), name="articles_details"),
    path("articles/like/<uuid:uuid>/", ArticleLikeAPIView.as_view(), name="articles_like"),
    path("articles/bookmark/<uuid:uuid>/", ArticleBookmarkAPIView.as_view(), name="articles_bookmark"),
    path("articles/share/<uuid:uuid>/", ArticleShareAPIView.as_view(), name="articles_share"),
]
