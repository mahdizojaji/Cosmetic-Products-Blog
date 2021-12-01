from django.contrib.auth import get_user_model
from django.db.models import Q
from itertools import chain
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from dj_rest_auth.views import UserDetailsView
from blog.models import Article, Course

from extensions.permissions import FullProfile, FullProfileOrReadOnly

from .serializers import UserSerializer, UserContentSerializer

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
        else:
            user_profile.liked_by.add(user)
        return Response(status=status.HTTP_200_OK)


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
        else:
            user_profile.bookmarked_by.add(user)
        return Response(status=status.HTTP_200_OK)


class UserIncreaseShareAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, FullProfile]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.share_qty += 1
        profile.save()
        return Response(status=status.HTTP_200_OK)


class UserContentsListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def list(self, request, *args, **kwargs):
        user = self.get_object()
        queryset = sorted(
            chain(
                Article.objects.filter(status=Article.PUBLISHED, author=user),
                Course.objects.filter(status=Course.PUBLISHED, author=user),
            ),
            key=lambda data: data.created_at,
            reverse=True,
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserContentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserContentSerializer(queryset, many=True)
        return Response(serializer.data)
