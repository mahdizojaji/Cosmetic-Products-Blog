from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField, ReadOnlyField, ListField, ImageField, FileField
)
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


class ArticleAbstractSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.uuid')
    status = ReadOnlyField(source='get_status_display')
    images = SerializerMethodField()
    videos = SerializerMethodField()

    def get_images(self, obj: Article):
        images = obj.images.filter(field_name=MediaFile.IMAGES)
        serializer = MediaFileSerializer(instance=images, many=True, context=self.context)
        return serializer.data

    def get_videos(self, obj: Article):
        videos = obj.videos.filter(field_name=MediaFile.VIDEOS)
        serializer = MediaFileSerializer(instance=videos, many=True, context=self.context)
        return serializer.data

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        videos = validated_data.pop('videos', [])
        instance: Article = super().create(validated_data)
        for image in images:
            MediaFile.objects.create(
                content_object=instance, file=image, field_name=MediaFile.IMAGES, author=instance.author,
            )
        for video in videos:
            MediaFile.objects.create(
                content_object=instance, file=video, field_name=MediaFile.VIDEOS, author=instance.author,
            )
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        videos = validated_data.pop('videos', [])
        instance: Article = super().update(instance, validated_data)
        instance.images.clear()
        instance.videos.clear()
        for image in images:
            MediaFile.objects.create(
                content_object=instance, file=image, field_name=MediaFile.IMAGES, author=instance.author,
            )
        for video in videos:
            MediaFile.objects.create(
                content_object=instance, file=video, field_name=MediaFile.VIDEOS, author=instance.author,
            )
        return instance


class ArticleSerializer(ArticleAbstractSerializer):
    # TODO: Fix: title is required in update articles
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
            "videos",
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
            "images",
            "videos",
        )


class ArticleWriteSerializer(ArticleAbstractSerializer):
    images = ListField(
        required=False,
        child=ImageField(required=False, allow_empty_file=False, use_url=False)
    )
    videos = ListField(
        required=False,
        child=FileField(required=False, allow_empty_file=False, use_url=False),
    )

    class Meta:
        model = Article
        exclude = ("id", "created_at", "updated_at")
        read_only_fields = ("uuid", "author", "slug", "status")
