from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # Articles
    # TODO: Fix all urls
    path("articles/", views.ArticleListCreateAPIView.as_view(), name="articles_list_create"),
    path("articles/<uuid:uuid>/", views.ArticleRetrieveUpdateDestroyAPIView.as_view(), name="articles_retrieve_update_destroy"),
    path("articles/like/<uuid:uuid>/", views.ArticleLikeAPIView.as_view(), name="articles_like"),
    path("articles/bookmark/<uuid:uuid>/", views.ArticleBookmarkAPIView.as_view(), name="articles_bookmark"),
    path("articles/share/<uuid:uuid>/", views.ArticleIncreaseShareAPIView.as_view(), name="articles_increase_share"),
    path("articles/publish/<uuid:uuid>/", views.ArticlePublishAPIView.as_view(), name="articles_publish"),
    # Courses
    path("courses/", views.CourseListCreateAPIView.as_view(), name="course_list_create"),
    path("courses/<uuid:uuid>/", views.CourseRetrieveAPIView.as_view(), name="course_retrieve"),
    path("courses/<uuid:uuid>/publish/", views.CoursePublishAPIView.as_view(), name="course_publish"),
    # TODO: Add comments & rate to courses
]
