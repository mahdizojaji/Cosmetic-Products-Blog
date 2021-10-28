from django.urls import path

from .views import ArticleList, ArticleDetails, ArticleLike, ArticleBookmark

app_name = "blog"

urlpatterns = [
    path("articles/list/", ArticleList.as_view(), name="articles_list"),
    path("articles/details/<uuid:uuid>", ArticleDetails.as_view(), name="articles_details"),
    path("articles/like/<uuid:uuid>/", ArticleLike.as_view(), name="articles_like"),
    path("articles/bookmark/<uuid:uuid>/", ArticleBookmark.as_view(), name="articles_bookmark"),
]
