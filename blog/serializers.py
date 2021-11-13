from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source="get_status_display", required=False)

    class Meta:
        model = Article
        fields = (
            "uuid",
            "author",
            "slug_title",
            "created_at",
            "updated_at",
            "likes",
            "bookmarks",
            "share_qty",
            "status",
            # ---
            "title",
            "content",
            "image",
        )
        read_only_fields = (
            "uuid",
            "author",
            "slug_title",
            "created_at",
            "updated_at",
            "likes",
            "bookmarks",
            "share_qty",
            "status",
        )
