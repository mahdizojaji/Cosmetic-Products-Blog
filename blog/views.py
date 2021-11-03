from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from django.forms.models import model_to_dict


from authentication.permissions import OwnerAndAdmin, OwnerAndAdminOrReadOnly
from .serializers import ArticleSerializer
from .models import Article

User = get_user_model()


class ArticleListCreateAPIView(ListCreateAPIView):
    """Create &  List Articles"""

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
    """Retrieve, Update & Delete Articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [OwnerAndAdminOrReadOnly]
    lookup_field = "uuid"

    def perform_update(self, serializer):
        admin = self.request.user.is_superuser
        status = serializer.instance.status

        if (status == Article.PENDING) and (not admin):
            return Response(
                {
                    "error": "article-pending",
                    "message": "You can't update a pending article.",
                    "detail": "Article is already pending.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif status == Article.PUBLISHED:
            if serializer.instance.clone:
                return Response(
                    {
                        "error": "article-pending",
                        "message": "You have to wait for previous changes.",
                        "detail": "Article is already submited for review.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            data = serializer.validated_data
            data["status"] = Article.PENDING
            Article.objects.create(**data)
        else:
            serializer.save()


class ArticlePublishAPIView(CreateAPIView):
    """Change Article Status to PUBLISHED"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [OwnerAndAdmin]
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        obj = self.get_object()
        admin = request.user.is_superuser
        # Only NON-Admin Authors can set PENDING status
        # (Asking for review from admins) ->
        if (not admin) and obj.status == Article.DRAFT:
            # if user is not admin then it must be auhtor
            obj.status = Article.PENDING
            obj.save()
        # Only Admin can publish articles with 'pending' status ->
        elif admin and obj.status == Article.PENDING:
            # By using clone mechanism, published articles remain
            # intact untill their clone get published.
            if original := obj.original:
                # replacing original article with clone data
                for field, value in model_to_dict(obj).items():
                    setattr(original, field, value)
                original.save()
                # removing temp clone
                obj.delete()
            else:
                obj.status = Article.PUBLISHED
                obj.save()
        else:
            detail = (
                "You dont have permission to publish a pending article."
                if obj.status == 1
                else "Article is already published"
            )
            # None of above case happends so its a bad request
            return Response(
                {
                    "error": "article-publish",
                    "message": "You have to be Admin or Article must be draft.",
                    "detail": detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # The happy ending! ->
        return Response(status=status.HTTP_200_OK)


class ArticleLikeAPIView(CreateAPIView):
    """Like & Unlike an Article"""

    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if Article.objects.filter(uuid=article.uuid, likes__in=[user]).exists():
            article.likes.remove(user)
        else:
            article.likes.add(user)
        return Response(status=status.HTTP_200_OK)


class ArticleBookmarkAPIView(CreateAPIView):
    """Bookmark & Un-bookmark an Article"""

    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if Article.objects.filter(uuid=article.uuid, bookmarks__in=[user]).exists():
            article.bookmarks.remove(user)
        else:
            article.bookmarks.add(user)
        return Response(status=status.HTTP_200_OK)


class ArticleIncreaseShareAPIView(CreateAPIView):
    """Increase Article Share Count"""

    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        article.share_qty += 1
        article.save()
        return Response(status=status.HTTP_200_OK)
