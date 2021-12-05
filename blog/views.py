from django.db.models import Q
from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)

from extensions.permissions import (
    OwnerAndAdmin,
    IsAdmin,
    FullProfile,
    FullProfileOrReadOnly,
)
from comments.views import CommentListCreateAbstractView
from comments.serializers import CommentSerializer, CommentAndRateSerializer
from config.settings import ARTICLE_CREDIT, PREMIUM_ARTICLE_CREDIT

from .models import Article, Course
from .filters import CourseFilter, ArticleFilter
from .serializers import (
    ArticleSerializer,
    ArticleWriteSerializer,
    OnlineCourseSerializer,
    OfflineCourseSerializer,
    CourseSerializer,
)

User = get_user_model()


class ArticleCommentListCreateAPIView(CommentListCreateAbstractView):
    queryset = Article.objects.filter(status=Article.PUBLISHED)
    serializer_class = CommentSerializer


class ArticleListCreateAPIView(ListCreateAPIView):
    """Create &  List Articles"""

    permission_classes = [FullProfileOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    filterset_class = ArticleFilter
    ordering_fields = ("-created_at",)
    search_fields = ("title", "content")

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
        query = Q(status=Article.PUBLISHED, premium=False)

        if self.request.user.is_authenticated:
            # include self articles
            query = Q(status=Article.PUBLISHED, premium=False) | Q(
                author=self.request.user
            )

            if self.request.user.subscription_expire > int(timezone.now().timestamp()):
                # include premium articles for vip users
                query = Q(status=Article.PUBLISHED) | Q(author=self.request.user)

        return Article.objects.filter(query)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = self.get_serializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleLikedListAPIView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ArticleFilter
    ordering_fields = ("-created_at",)

    def get_queryset(self):
        return Article.objects.filter(liked_by=self.request.user)


class ArticleBookmarkedListAPIView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ArticleFilter
    ordering_fields = ("-created_at",)

    def get_queryset(self):
        return Article.objects.filter(bookmarked_by=self.request.user)


class ArticleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Retrieve, Update & Delete Articles"""

    permission_classes = [FullProfileOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
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
        if self.request.user.is_superuser:
            return Article.objects.all()

        query = Q(status=Article.PUBLISHED, premium=False)

        if self.request.user.is_authenticated:
            # include self articles
            query = Q(status=Article.PUBLISHED, premium=False) | Q(
                author=self.request.user
            )

            if self.request.user.subscription_expire > int(timezone.now().timestamp()):
                # include premium articles for vip users
                query = Q(status=Article.PUBLISHED) | Q(author=self.request.user)

        return Article.objects.filter(query)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        admin = self.request.user.is_superuser
        _status = serializer.instance.status

        if (_status == Article.PENDING) and (not admin):
            # preventing update of published article
            return Response(
                {
                    "error": "article-pending",
                    "message": "You can't update a pending article.",
                    "detail": "Article is already pending.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif _status == Article.PUBLISHED:
            if hasattr(instance, "clone"):
                # preventing update of published article
                return Response(
                    {
                        "error": "article-pending",
                        "message": "You have to wait for previous changes.",
                        "detail": "Article is already submited for review.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            # creating temporary clone from input instance
            data = serializer.validated_data
            data["status"] = Article.PENDING
            data["original"] = instance
            Article.objects.create(**data)
            # instance remaind intact
        else:
            # unlimited normal update for draft articles
            self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ArticlePublishAPIView(GenericAPIView):
    """Change Article Status to PUBLISHED"""

    queryset = Article.objects.filter(status__in=[Article.DRAFT, Article.PENDING])
    serializer_class = ArticleSerializer
    permission_classes = [OwnerAndAdmin]
    lookup_field = "uuid"

    def publish(self):
        if not self.obj.content:
            self.detail = "Article content is required."
            return

        if original := self.obj.original:
            update_fields = ("title", "content", "images", "videos")
            # By using clone mechanism, published articles remain
            # intact until their clone get published.
            for field, value in model_to_dict(self.obj).items():
                if field in update_fields and value:
                    # replacing original article with clone data
                    setattr(original, field, value)
            original.edited_at = timezone.now()
            original.save()
            # removing temp clone
            self.obj.delete()
        else:
            self.obj.status = Article.PUBLISHED
            self.obj.edited_at = self.obj.published_at = timezone.now()
            self.obj.save()

            # credit
            self.obj.author.credit += (
                PREMIUM_ARTICLE_CREDIT if self.obj.premium else ARTICLE_CREDIT
            )
            self.obj.author.save()

    def get(self, request, *args, **kwargs):
        self.detail = None
        obj = self.obj = self.get_object()
        # DRAFT
        if obj.status is Article.DRAFT:
            if request.user.is_superuser:
                # goes straight to publish
                self.publish()
            else:
                # only gets pending
                obj.status = Article.PENDING
                obj.save()
        # PENDING
        else:
            if request.user.is_superuser:
                # publish
                self.publish()
            else:
                self.detail = "You dont have permission to publish articles."

        if self.detail:
            return Response(
                {
                    "error": "article-publish",
                    "message": "You cant publish this article.",
                    "detail": self.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)


class ArticleLikeAPIView(CreateAPIView):
    """Like & Unlike an Article"""

    permission_classes = [FullProfile]
    queryset = Article.objects.filter(status=Article.PUBLISHED)
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if Article.objects.filter(uuid=article.uuid, liked_by__in=[user]).exists():
            article.liked_by.remove(user)
        else:
            article.liked_by.add(user)
        return Response(status=status.HTTP_200_OK)


class ArticleBookmarkAPIView(CreateAPIView):
    """Bookmark & Un-bookmark an Article"""

    permission_classes = [FullProfile]
    queryset = Article.objects.filter(status=Article.PUBLISHED)
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        if Article.objects.filter(uuid=article.uuid, bookmarked_by__in=[user]).exists():
            article.bookmarked_by.remove(user)
        else:
            article.bookmarked_by.add(user)
        return Response(status=status.HTTP_200_OK)


class ArticleIncreaseShareAPIView(CreateAPIView):
    """Increase Article Share Count"""

    permission_classes = [FullProfile]
    queryset = Article.objects.filter(status=Article.PUBLISHED)
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        article = self.get_object()
        article.share_qty += 1
        article.save()
        return Response(status=status.HTTP_200_OK)


class CourseListCreateAPIView(ListCreateAPIView):
    """List & Create Course"""

    permission_classes = [FullProfileOrReadOnly]
    filterset_class = CourseFilter
    search_fields = ("title", "content")
    ordering_fields = ("-created_at",)
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

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
        if self.request.user.is_authenticated:
            return Course.objects.filter(
                Q(author=self.request.user) | Q(status=Course.PUBLISHED)
            )
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
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            is_online=True if self.course_method == "online" else False,
        )


class CourseRetrieveAPIView(RetrieveAPIView):
    """Course Details"""

    lookup_field = "uuid"
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Course.objects.all()
            else:
                return Course.objects.filter(
                    Q(author=self.request.user) | Q(status=Course.PUBLISHED)
                )
        return Course.objects.filter(status=Course.PUBLISHED)


class CoursePublishAPIView(GenericAPIView):
    """Change course Status to PUBLISHED"""

    queryset = Course.objects.filter(status=Course.PENDING)
    serializer_class = CourseSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uuid"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = Article.PUBLISHED
        obj.published_at = timezone.now()
        obj.save()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseCommentListCreateAPIView(CommentListCreateAbstractView):
    queryset = Course.objects.filter(status=Course.PUBLISHED)
    serializer_class = CommentAndRateSerializer
