from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from dj_rest_auth.views import UserDetailsView
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import OwnerAndAdmin, OwnerAndAdminOrReadOnly
from .serializers import (
    UserDetailsSerializer,
    UserProfileFullSerializer,
    UserProfileLimitedSerializer,
)

User = get_user_model()


class UserDetailsAPIView(UserDetailsView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]


class UserProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = "uuid"

    def get_serializer_class(self):
        if OwnerAndAdmin().has_object_permission(
            request=self.request, view=self, obj=self.get_object()
        ):
            return UserProfileFullSerializer

        return UserProfileLimitedSerializer


class UserLikeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user = request.user
        if user in user_profile.liked_by.all():
            user_profile.liked_by.remove(user)
        else:
            user_profile.liked_by.add(user)
        return Response(status=status.HTTP_200_OK)


class UserBookmarkAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user = request.user
        if user in user_profile.bookmarked_by.all():
            user_profile.bookmarked_by.remove(user)
        else:
            user_profile.bookmarked_by.add(user)
        return Response(status=status.HTTP_200_OK)


class UserShareAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.share_qty += 1
        profile.save()
        return Response(status=status.HTTP_200_OK)
