from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from dj_rest_auth.views import UserDetailsView

from comments.models import Comment
from blog.models import Article, Course
from extensions.permissions import FullProfile, FullProfileOrReadOnly

from .serializers import UserSerializer, AuthorCommentsSerializer

User = get_user_model()


class UserDetailsRetrieveUpdateAPIView(UserDetailsView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, FullProfileOrReadOnly]
    queryset = User.objects.all()
    lookup_field = "uuid"


class UserLikeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, FullProfile]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user = request.user
        if User.objects.filter(uuid=user_profile.uuid, liked_by__in=[user]).exists():
            user_profile.liked_by.remove(user)
            return Response({"is_liked": False}, status=status.HTTP_200_OK)
        else:
            user_profile.liked_by.add(user)
            return Response({"is_liked": True}, status=status.HTTP_200_OK)


class UserBookmarkAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, FullProfile]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user = request.user
        if User.objects.filter(
            uuid=user_profile.uuid, bookmarked_by__in=[user]
        ).exists():
            user_profile.bookmarked_by.remove(user)
            return Response({"is_bookmarked": False}, status=status.HTTP_200_OK)
        else:
            user_profile.bookmarked_by.add(user)
            return Response({"is_bookmarked": True}, status=status.HTTP_200_OK)


class UserIncreaseShareAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, FullProfile]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.share_qty += 1
        profile.save()
        return Response(status=status.HTTP_200_OK)


class AuthorCommentsAPIView(ListAPIView):
    serializer_class = AuthorCommentsSerializer

    def get_queryset(self):
        author = get_object_or_404(User, uuid=self.kwargs["uuid"])
        query = None
        articles_ids = Article.objects.filter(author=author).values_list("id", flat=True)
        courses_ids = Course.objects.filter(author=author).values_list("id", flat=True)
        if articles_ids:
            query = Q(object_id__in=articles_ids, content_type__model=Article.__name__.lower())
        if courses_ids:
            course_query = Q(object_id__in=courses_ids, content_type__model=Course.__name__.lower())
            if query:
                query |= course_query
            else:
                query = course_query
        if query:
            return Comment.objects.filter(query)
        return Comment.objects.none()
