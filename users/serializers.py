from rest_framework.fields import IntegerField
from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
)
from django.contrib.auth import get_user_model

from authentication.permissions import OwnerAndAdmin

User = get_user_model()


class UserDetailsSerializer(ModelSerializer):
    shares = IntegerField(source="share_qty", read_only=True)
    likes = IntegerField(source="liked_by.count", read_only=True)
    bookmarks = IntegerField(source="bookmarked_by.count", read_only=True)

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
            "shares",
            "likes",
            "bookmarks",
        )
        read_only_fields = ("uuid", "phone_number", "shares", "likes", "bookmarks")


class UserProfileSerializer(ModelSerializer):
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
            "liked_by",
            "bookmarked_by",
            "rates",
            "share_qty",
            "vip_expire",
            "is_superuser",
        )
        private_fields = (
            "phone_number",
            "email",
            "birth_date",
            "vip_expire",
            "is_superuser",
        )

    def get_fields(self):
        full = super().get_fields()
        fields = {}
        access = OwnerAndAdmin().has_object_permission(
            request=self.context["request"], view=self, obj=self.instance
        )
        for key, value in full.items():
            if key not in self.Meta.private_fields or access:
                fields[key] = value
                fields[key].read_only = True
        return fields
