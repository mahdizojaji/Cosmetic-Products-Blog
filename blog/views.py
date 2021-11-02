from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)


from authentication.permissions import OwnerAndAdminOrReadOnly
from .serializers import ArticleSerializer
from .models import Article

User = get_user_model()


class ArticleListCreateAPIView(ListCreateAPIView):
    """Create &  List Articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = (
        "author",
        "title",
        "content",
        "slug_title",
    )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, Update & Delete Articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [OwnerAndAdminOrReadOnly]
    lookup_field = "uuid"


class ArticleLikeAPIView(CreateAPIView):
    """Like & Unlike an Article
    """
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if user in article.likes.all():  # TODO: Fix Query
            article.likes.remove(user)
        else:
            article.likes.add(user)
        return Response(status=status.HTTP_200_OK)


class ArticleBookmarkAPIView(CreateAPIView):
    """Bookmark & Un-bookmark an Article
    """
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if user in article.bookmarks.all():  # TODO: Fix Query
            article.bookmarks.remove(user)
        else:
            article.bookmarks.add(user)
        return Response(status=status.HTTP_200_OK)


# Increase an Article's share
class ArticleIncreaseShareAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        article.share_qty += 1
        article.save()
        return Response(status=status.HTTP_200_OK)
