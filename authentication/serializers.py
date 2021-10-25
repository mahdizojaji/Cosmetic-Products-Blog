from rest_framework.serializers import ModelSerializer
from .models import User


class SendCodeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number",)
        extra_kwargs = {"phone_number": {"validators": [User.phone_number_validator]}}


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number", "password")
        extra_kwargs = {"phone_number": {"validators": [User.phone_number_validator]}}


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
            "email",
            "birth_date",
            "fname",
            "lname",
            "avatar_img",
            "cover_img",
            "province",
            "city",
        )


class UserProfileLimitedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "fname",
            "lname",
            "avatar_img",
            "cover_img",
            "province",
        )
