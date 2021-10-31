from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailsSerializer(ModelSerializer):
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
        )
        read_only_fields = ("uuid", "phone_number")


class UserProfileFullSerializer(ModelSerializer):
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

    def get_fields(self):
        fields = super().get_fields() 
        for field in fields.values():
            field.read_only = True
        return fields    


class UserProfileLimitedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
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
        )

    def get_fields(self):
        fields = super().get_fields() 
        for field in fields.values():
            field.read_only = True
        return fields
