from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from .models import Article


class ArticleSerializer(ModelSerializer):
    status = CharField(source="get_status_display", required=False)

    class Meta:
        model = Article
        fields = (
            "uuid",
            "author",
            "slug",
            "created_at",
            "updated_at",
            "likes",
            "bookmarks",
            "share_qty",
            "status",
            "rate",
            "rate_counts",
            # ---
            "title",
            "content",
            "image",
        )
        read_only_fields = (
            "uuid",
            "author",
            "slug",
            "created_at",
            "updated_at",
            "likes",
            "bookmarks",
            "share_qty",
            "status",
            "rate",
            "rate_counts",
        )
