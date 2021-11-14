from rest_framework import serializers

from extensions.serializer_fields import TimestampField
from extensions.validators import FutureDateValidator

from .models import Article, Course, MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.uuid')
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.file.url)

    class Meta:
        model = MediaFile
        fields = ("uuid", "author", "url")


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


class CourseAbstractSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.uuid')
    status = serializers.ReadOnlyField(source='get_status_display')
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
    sessions = serializers.SerializerMethodField()

    def get_sessions(self, obj: Course):
        sessions = obj.videos.filter(field_name=MediaFile.SESSIONS)
        serializer = MediaFileSerializer(instance=sessions, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Course
        exclude = ("id", "address", "deadline", "created_at", "updated_at")
        read_only_fields = ("uuid", "author", "slug", "status", "is_online")


class OfflineCourseSerializer(CourseAbstractSerializer):
    deadline = TimestampField(required=False, validators=[FutureDateValidator()])

    class Meta:
        model = Course
        exclude = ("id", "created_at", "updated_at")
        read_only_fields = ("uuid", "author", "slug", "status", "is_online")
