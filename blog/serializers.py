from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Article


class ArticleSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Article
        fields = (
            "uuid",
            "author",
            "created_at",
            "updated_at",
            "likes",
            "bookmarks",
            "share_qty",
            "status",
            # ---
            "title",
            "slug_title",
            "content",
            "image",
        )
        read_only_fields = (
            "uuid",
            "author",
            "created_at",
            "updated_at",
            "likes",
            "bookmarks",
            "share_qty",
            "status",
        )
