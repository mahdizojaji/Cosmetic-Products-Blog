from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer

User = get_user_model()


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


class LoginUserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid","phone_number")
        read_only_fields = ("uuid","phone_number")

        