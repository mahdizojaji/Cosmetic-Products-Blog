from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # Articles
    path("articles/", views.ArticleListCreateAPIView.as_view(), name="articles_list_create"),
    path("articles/<uuid:uuid>/", views.ArticleRetrieveUpdateDestroyAPIView.as_view(),
         name="articles_retrieve_update_destroy"),
    path("articles/<uuid:uuid>/like/", views.ArticleLikeAPIView.as_view(), name="articles_like"),
    path("articles/<uuid:uuid>/bookmark/", views.ArticleBookmarkAPIView.as_view(), name="articles_bookmark"),
    path("articles/<uuid:uuid>/share/", views.ArticleIncreaseShareAPIView.as_view(), name="articles_increase_share"),
    path("articles/<uuid:uuid>/publish/", views.ArticlePublishAPIView.as_view(), name="articles_publish"),
    path("articles/<uuid:uuid>/comments/", views.ArticleCommentListCreateAPIView.as_view(),
         name="comments_list_create"),
    # Courses
    path("courses/", views.CourseListCreateAPIView.as_view(), name="course_list_create"),
    path("courses/<uuid:uuid>/", views.CourseRetrieveAPIView.as_view(), name="course_retrieve"),
    path("courses/<uuid:uuid>/publish/", views.CoursePublishAPIView.as_view(), name="course_publish"),
    # TODO: Add comments & rate to courses
]
