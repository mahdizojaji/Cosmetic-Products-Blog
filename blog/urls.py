from django.urls import path

from .views import *

app_name = "blog"

urlpatterns = [
    # Articles
    path("articles/", ArticleListCreateAPIView.as_view(), name="articles_list_create"),
    path("articles/pending/", ArticlePendingListAPIView.as_view(), name="articles_pending_list"),
    path("articles/liked/", ArticleLikedListAPIView.as_view(), name="articles_liked_list"),
    path("articles/bookmarked/", ArticleBookmarkedListAPIView.as_view(), name="articles_bookmarked_list"),
    path("articles/<uuid:uuid>/", ArticleRetrieveUpdateDestroyAPIView.as_view(), name="articles_retrieve_update_destroy"),
    path("articles/<uuid:uuid>/like/", ArticleLikeAPIView.as_view(), name="articles_like"),
    path("articles/<uuid:uuid>/bookmark/", ArticleBookmarkAPIView.as_view(), name="articles_bookmark"),
    path("articles/<uuid:uuid>/share/", ArticleIncreaseShareAPIView.as_view(), name="articles_increase_share"),
    path("articles/<uuid:uuid>/publish/", ArticlePublishAPIView.as_view(), name="articles_publish"),
    path("articles/<uuid:uuid>/comments/", ArticleCommentListCreateAPIView.as_view(), name="articles_comments_list_create"),
    # Courses
    path("courses/", CourseListCreateAPIView.as_view(), name="course_list_create"),
    path("courses/pending/", CoursePendingListAPIView.as_view(), name="course_pending_list"),
    path("courses/<uuid:uuid>/", CourseRetrieveAPIView.as_view(), name="course_retrieve"),
    path("courses/<uuid:uuid>/publish/", CoursePublishAPIView.as_view(), name="course_publish"),
    path("courses/<uuid:uuid>/comments/", CourseCommentListCreateAPIView.as_view(), name="course_comments_list_create"),
]
