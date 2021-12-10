from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from rest_framework import serializers

from comments.models import Comment
from extensions.permissions import OwnerAndAdmin
from extensions.serializer_fields import TimestampField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    comment_counts = serializers.IntegerField(source="comment_qty", read_only=True)
    share_counts = serializers.IntegerField(source="share_qty", read_only=True)
    likes = serializers.IntegerField(source="liked_by.count", read_only=True)
    bookmarks = serializers.IntegerField(source="bookmarked_by.count", read_only=True)
    birth_date = TimestampField()

    def get_comment_counts(self, obj):
        return obj.comments.count()

    class Meta:
        model = User
        fields = (
            "uuid",
            "phone_number",
            "email",
            "birth_date",
            "fname",
            "lname",
            "avatar_img",
            "cover_img",
            "province",
            "city",
            "likes",
            "bookmarks",
            "rate",
            "rate_counts",
            "comment_counts",
            "share_counts",
            "job_title",
            "bio",
            "subscription_expire",
            "is_superuser",
            "credit",
        )
        private_fields = (
            "phone_number",
            "email",
            "birth_date",
            "subscription_expire",
            "is_superuser",
        )
        read_only_fields = (
            "uuid",
            "phone_number",
            "likes",
            "bookmarks",
            "rate",
            "rate_counts",
            "comment_counts",
            "share_counts",
            "subscription_expire",
            "is_superuser",
            "credit",
        )

    def get_fields(self):
        fields = {}
        access = OwnerAndAdmin().has_object_permission(
            request=self.context["request"], view=self, obj=self.instance
        )
        for key, value in super().get_fields().items():
            if access:
                fields[key] = value
                if key in self.Meta.read_only_fields:
                    fields[key].read_only = True
            elif key not in self.Meta.private_fields:
                fields[key] = value
                fields[key].read_only = True
        return fields


class AuthorReadOnlySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj: User):
        return self.context["request"].build_absolute_uri(obj.reverse_url())

    class Meta:
        model = User
        fields = ("uuid", "avatar_img", "name", "bio", "job_title", "url")


class AuthorCommentsSerializer(serializers.ModelSerializer):
    object_url = serializers.SerializerMethodField()

    def get_object_url(self, obj: Comment):
        request = self.context["request"]
        if obj.content_type.model == 'article':
            return request.build_absolute_uri(
                reverse('blog:articles_retrieve_update_destroy', args=(obj.content_object.uuid,))
            )
        elif obj.content_type.model == 'course':
            return request.build_absolute_uri(reverse('blog:course_retrieve', args=(obj.content_object.uuid,)))
        return ''

    class Meta:
        model = Comment
        fields = ("uuid", "author", "text", "rate", "object_url", "created_at", "updated_at")
