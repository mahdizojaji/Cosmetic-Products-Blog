from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    """
    Serializer for the Comment model.
    """
    author = ReadOnlyField(source='author.uuid')

    class Meta:
        model = Comment
        fields = ("uuid", "text", "author", "created_at")
        read_only_fields = ("uuid", "author", "created_at")
