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
        fields = ("uuid", "phone_number", "email")
        read_only_fields = ("phone_number",)
