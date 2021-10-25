from django.urls import path

from .views import ArticleList, ArticleDetails, ArticleLike

app_name = "blog"

urlpatterns = [
    path("articles/list/", ArticleList.as_view(), name="articles_list"),
    path("articles/details/<uuid:uuid>", ArticleDetails.as_view(), name="articles_details"),
    path("articles/like/<uuid:uuid>example/", ArticleLike.as_view(), name="articles_like"),
]
