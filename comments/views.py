from django.utils import timezone

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from extensions.permissions import OwnerOrAdminOrAuthorOrReadOnly

from .models import Comment
from .serializers import CommentSerializer, CommentAndRateSerializer


class CommentListCreateAbstractView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment(
            content_object=self.get_object(),
            author=request.user,
            text=serializer.validated_data["text"],
            rate=serializer.validated_data.get("rate"),
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


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentAndRateSerializer
    lookup_field = "uuid"
    permission_classes = [OwnerOrAdminOrAuthorOrReadOnly]
