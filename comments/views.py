from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import OwnerAndAdminOrReadOnly
from django.utils import timezone

from .serializers import (
    CommentSerializer,
)
from .models import Comment


class CommentListCreateAbstractView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment(
            content_object=self.get_object(),
            author=request.user,
            text=serializer.validated_data["text"],
            rate=serializer.validated_data["rate"],
            created_at=timezone.now(),
        )
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_object().comments.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "uuid"
    permission_classes = [OwnerAndAdminOrReadOnly]
"""
