from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    """
    Serializer for the Comment model.
    """

    author = ReadOnlyField(source="author.uuid")
    related = ReadOnlyField(source="content_object.uuid")

    class Meta:
        model = Comment
        fields = ("uuid", "author", "related", "created_at", "text", "rate")
        read_only_fields = ("uuid", "author", "related", "created_at")
