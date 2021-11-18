from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from extensions.serializer_fields import TimestampField
from extensions.validators import FutureDateValidator

from .models import Article, Course, MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.uuid")
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(obj.file.url)

    class Meta:
        model = MediaFile
        fields = ("uuid", "author", "url")


class ArticleAbstractSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.uuid")
    status = serializers.ReadOnlyField(source="get_status_display")
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    def get_images(self, obj: Article):
        images = obj.images.filter(field_name=MediaFile.IMAGES)
        serializer = MediaFileSerializer(instance=images, many=True, context=self.context)
        return serializer.data

    def get_videos(self, obj: Article):
        videos = obj.videos.filter(field_name=MediaFile.VIDEOS)
        serializer = MediaFileSerializer(instance=videos, many=True, context=self.context)
        return serializer.data

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        videos = validated_data.pop("videos", [])
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
        images = validated_data.pop("images", [])
        videos = validated_data.pop("videos", [])
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
    class Meta:
        model = Article
        fields = (
            "uuid", "author", "slug", "created_at", "updated_at", "likes", "bookmarks", "share_qty", "status", "rate",
            "rate_counts", "title", "content", "images", "videos",
        )
        read_only_fields = (
            "uuid", "author", "slug", "created_at", "updated_at", "likes", "bookmarks", "share_qty", "status", "rate",
            "rate_counts", "images", "videos",
        )


class ArticleWriteSerializer(ArticleAbstractSerializer):
    images = serializers.ListField(
        required=False,
        child=serializers.ImageField(required=False, allow_empty_file=False, use_url=False)
    )
    videos = serializers.ListField(
        required=False,
        child=serializers.FileField(required=False, allow_empty_file=False, use_url=False),
    )

    class Meta:
        model = Article
        exclude = ("id", "created_at", "updated_at")
        read_only_fields = ("uuid", "author", "slug", "status")


class CourseAbstractSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.uuid")
    status = serializers.ReadOnlyField(source="get_status_display")
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    def get_images(self, obj: Course):
        images = obj.images.filter(field_name=MediaFile.IMAGES)
        serializer = MediaFileSerializer(instance=images, many=True, context=self.context)
        return serializer.data

    def get_videos(self, obj: Course):
        videos = obj.videos.filter(field_name=MediaFile.VIDEOS)
        serializer = MediaFileSerializer(instance=videos, many=True, context=self.context)
        return serializer.data

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        videos = validated_data.pop("videos", [])
        instance: Course = super().create(validated_data)
        for image in images:
            MediaFile.objects.create(
                content_object=instance, file=image, field_name=MediaFile.IMAGES, author=instance.author,
            )
        for video in videos:
            MediaFile.objects.create(
                content_object=instance, file=video, field_name=MediaFile.VIDEOS, author=instance.author,
            )
        return instance


class CourseSerializer(CourseAbstractSerializer):
    sessions = serializers.SerializerMethodField()
    deadline = TimestampField(required=False, validators=[FutureDateValidator()])

    def get_sessions(self, obj: Course):
        sessions = obj.videos.filter(field_name=MediaFile.SESSIONS)
        serializer = MediaFileSerializer(instance=sessions, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Course
        exclude = ("id", "created_at", "updated_at")


class OnlineCourseSerializer(CourseAbstractSerializer):
    images = serializers.ListField(
        required=True,
        child=serializers.ImageField(required=False)
    )
    videos = serializers.ListField(
        required=True,
        child=serializers.FileField(required=False, allow_empty_file=False, use_url=False),
    )
    sessions = serializers.ListField(
        required=False,
        child=serializers.FileField(required=False, allow_empty_file=False, use_url=False),
    )

    def validate(self, attrs):
        super().validate(attrs)
        if attrs["quantity"] != len(attrs["sessions"]):
            raise ValidationError(
                detail={
                    "sessions": f"quantity({attrs['quantity']}) not equal quantity of sessions"
                                f"({len(attrs['sessions'])})",
                },
            )
        return attrs

    def create(self, validated_data):
        sessions = validated_data.pop("sessions", [])
        instance: Course = super().create(validated_data)
        for session in sessions:
            MediaFile.objects.create(
                content_object=instance, file=session, field_name=MediaFile.SESSIONS, author=instance.author,
            )
        return instance

    class Meta:
        model = Course
        exclude = ("id", "address", "deadline", "created_at", "updated_at")
        read_only_fields = ("uuid", "author", "slug", "status", "is_online")
        extra_kwargs = {
            "content": {"required": True},
            "cost": {"required": True},
        }


class OfflineCourseSerializer(CourseAbstractSerializer):
    deadline = TimestampField(required=True, validators=[FutureDateValidator()])
    images = serializers.ListField(
        required=False,
        child=serializers.ImageField(required=False)
    )
    videos = serializers.ListField(
        required=False,
        child=serializers.FileField(required=False, allow_empty_file=False, use_url=False),
    )

    class Meta:
        model = Course
        exclude = ("id", "created_at", "updated_at")
        read_only_fields = ("uuid", "author", "slug", "status", "is_online")
        extra_kwargs = {
            "content": {"required": True},
            "cost": {"required": True},
            "address": {"required": True},
        }
