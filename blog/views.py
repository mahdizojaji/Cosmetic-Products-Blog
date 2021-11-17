from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView
)

from extensions.permissions import OwnerAndAdmin, OwnerAndAdminOrReadOnly, IsAdmin
from comments.views import CommentListCreateAbstractView
from comments.serializers import CommentSerializer, CommentAndRateSerializer

from .models import Article, Course
from .filters import CourseFilter
from .serializers import (
    ArticleSerializer, ArticleWriteSerializer, OnlineCourseSerializer, OfflineCourseSerializer, CourseSerializer
)

User = get_user_model()


class ArticleCommentListCreateAPIView(CommentListCreateAbstractView):
    queryset = Article.objects.all()
    serializer_class = CommentSerializer


class ArticleListCreateAPIView(ListCreateAPIView):
    """Create &  List Articles"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser,)
    filterset_fields = ("author", "title", "content", "slug")
    ordering_fields = ("-created_at", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None

    def get_serializer(self, *args, **kwargs):
        self.data = kwargs.get("data")
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.data:
            return ArticleWriteSerializer
        return ArticleSerializer

    def get_queryset(self):
        if isinstance(self.request.user, get_user_model()):
            return Article.objects.filter(
                Q(author=self.request.user) | Q(status=Article.PUBLISHED)
            )
        return Article.objects.filter(status=Article.PUBLISHED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = self.get_serializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, Update & Delete Articles"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser,)
    lookup_field = "uuid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None

    def get_serializer(self, *args, **kwargs):
        self.data = kwargs.get("data")
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.data:
            return ArticleWriteSerializer
        return ArticleSerializer

    def get_queryset(self):
        if isinstance(self.request.user, get_user_model()):
            return Article.objects.filter(Q(author=self.request.user) | Q(status=Article.PUBLISHED))
        return Article.objects.filter(status=Article.PUBLISHED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        admin = self.request.user.is_superuser
        _status = serializer.instance.status

        if (_status == Article.PENDING) and (not admin):
            return Response(
                {
                    "error": "article-pending",
                    "message": "You can't update a pending article.",
                    "detail": "Article is already pending.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif _status == Article.PUBLISHED:
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

        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# TODO: Use GenericAPIView instead CreateAPIView for some views
class ArticlePublishAPIView(CreateAPIView):
    """Change Article Status to PUBLISHED"""

    # TODO: Check all required fields are filled

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
            # if user is not admin then it must be author
            obj.status = Article.PENDING
            obj.save()
        # Only Admin can publish articles with 'pending' status ->
        elif admin and obj.status == Article.PENDING:
            # By using clone mechanism, published articles remain
            # intact until their clone get published.
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
            # None of above case happens so its a bad request
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


class CourseListCreateAPIView(ListCreateAPIView):
    """List & Create Course"""
    # TODO: Convert some Authenticated permissions to FullProfile Permission
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = CourseFilter
    search_fields = ("title", "content")
    parser_classes = (MultiPartParser, FormParser,)

    # TODO: check is seller or vip (hide sessions & addresses for non-vip)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_method = None
        self.data = None

    def get_serializer(self, *args, **kwargs):
        self.data = kwargs.get("data")
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.course_method == "online" and self.data:
            return OnlineCourseSerializer
        elif self.course_method == "offline" and self.data:
            return OfflineCourseSerializer
        return CourseSerializer

    def get_queryset(self):
        if isinstance(self.request.user, get_user_model()):
            return Course.objects.filter(Q(author=self.request.user) | Q(status=Course.PUBLISHED))
        return Course.objects.filter(status=Course.PUBLISHED)

    def create(self, request, *args, **kwargs):
        self.course_method = self.request.query_params.get("method")
        if self.course_method not in ("online", "offline"):
            return Response(
                data={
                    "error": "course-method",
                    "message": "You should set course method.",
                    "detail": "method=online or method=offline in query_params",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        serializer = self.get_serializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            is_online=True if self.course_method == "online" else False
        )


class CourseRetrieveAPIView(RetrieveAPIView):
    """Course Details"""
    queryset = Course.objects.all()
    lookup_field = "uuid"
    serializer_class = CourseSerializer


class CoursePublishAPIView(GenericAPIView):
    """Change course Status to PUBLISHED"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uuid"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = Article.PUBLISHED
        obj.save()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseCommentListCreateAPIView(CommentListCreateAbstractView):
    queryset = Course.objects.all()
    serializer_class = CommentAndRateSerializer
