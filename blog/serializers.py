from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, SerializerMethodField,ReadOnlyField
from .models import Article, MediaFile


class MediaFileSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.uuid')
    url = SerializerMethodField()

    def get_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.file.url)

    class Meta:
        model = MediaFile
        fields = ("uuid", "author", "url")


class ArticleSerializer(ModelSerializer):
    status = CharField(source="get_status_display", required=False)
    images = SerializerMethodField()
    
    def get_images(self, obj: Article):
        images = obj.images.filter(field_name=MediaFile.IMAGES)
        serializer = MediaFileSerializer(instance=images, many=True, context=self.context)
        return serializer.data

    
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
            "images",
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
