from django.contrib.auth import get_user_model

from rest_framework import serializers

from extensions.permissions import OwnerAndAdmin

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    shares = serializers.IntegerField(source="share_qty", read_only=True)
    likes = serializers.IntegerField(source="liked_by.count", read_only=True)
    bookmarks = serializers.IntegerField(source="bookmarked_by.count", read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid", "phone_number", "email", "birth_date", "fname", "lname", "avatar_img", "cover_img", "province",
            "city", "shares", "likes", "bookmarks", "vip_expire", "is_superuser",
        )
        private_fields = ("phone_number", "email", "birth_date", "vip_expire", "is_superuser")
        read_only_fields = ("uuid", "phone_number", "shares", "likes", "bookmarks", "vip_expire", "is_superuser")

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
