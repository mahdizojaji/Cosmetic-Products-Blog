from rest_framework.serializers import ModelSerializer
from .models import Article


class ArticleSerializer(ModelSerializer):
    class Meta:

        model = Article
        fields = (
            "uuid",
            "title",
            "content",
            "image",
            "created_at",
            "updated_at",
            "slug_title",
        )
        read_only_fields = ("uuid", "slug_title", "created_at", "updated_at")
        lookup_field = "uuid"
