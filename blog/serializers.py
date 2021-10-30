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
            "bookmarks",
            "share_qty",
        )
        read_only_fields = (
            "uuid",
            "author",
            "likes",
            "bookmarks",
            "share_qty",
            "created_at",
            "updated_at",
        )
