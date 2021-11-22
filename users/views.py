from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from dj_rest_auth.views import UserDetailsView

from extensions.permissions import FullProfile, FullProfileOrReadOnly


from .serializers import UserSerializer

User = get_user_model()


class UserDetailsRetrieveUpdateAPIView(UserDetailsView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [FullProfileOrReadOnly]
    queryset = User.objects.all()
    lookup_field = "uuid"


class UserLikeAPIView(CreateAPIView):
    permission_classes = [FullProfile]
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
    permission_classes = [FullProfile]
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
    permission_classes = [FullProfile]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.share_qty += 1
        profile.save()
        return Response(status=status.HTTP_200_OK)
