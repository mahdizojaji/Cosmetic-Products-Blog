from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)

from authentication.permissions import OwnerAndAdminOrReadOnly, OwnerAndAdmin
from .serializers import ArticleSerializer
from .models import Article

User = get_user_model()

# Create &  List Articles
class ArticleList(ListCreateAPIView):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


# Retrieve, Update & Delete Articles
class ArticleDetails(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [OwnerAndAdminOrReadOnly]
    lookup_field = "uuid"


# Like & Unlike an Article
class ArticleLike(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if user in article.likes.all():
            article.likes.remove(user)
        else:
            article.likes.add(user)
        return Response(status=status.HTTP_200_OK)


# Bookmark & Unbookmark an Article
class ArticleBookmark(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if user in article.bookmarks.all():
            article.bookmarks.remove(user)
        else:
            article.bookmarks.add(user)
        return Response(status=status.HTTP_200_OK)
