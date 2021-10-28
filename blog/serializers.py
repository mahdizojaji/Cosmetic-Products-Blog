from rest_framework.serializers import ModelSerializer
from .models import Article


class ArticleSerializer(ModelSerializer):
    class Meta:

        model = Article
        fields = (
            "uuid",
            "author",
            "title",
            "content",
            "image",
            "created_at",
            "updated_at",
            "slug_title",
            "likes",
        )
        read_only_fields = (
            "uuid",
            "author",
            "slug_title",
            "likes",
            "created_at",
            "updated_at",
        )
        lookup_field = "uuid"
