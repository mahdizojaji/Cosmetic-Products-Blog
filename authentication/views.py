from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.core.cache import cache
from config.settings import OTP_EXPIRE, SMS
from rest_framework.response import Response
from dj_rest_auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)
from dj_rest_auth.utils import jwt_encode

from .serializers import SendCodeSerializer, LoginSerializer
from extensions.sms import generate_random_code

User = get_user_model()


class SendCode(CreateAPIView):
    serializer_class = SendCodeSerializer

    def create(self, request, *args, **kwargs):
        # generating random code
        otp = "123456" if SMS["DEBUG_MODE"] else str(generate_random_code())
        # validating serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get or create user
        user, _ = User.objects.get_or_create(
            phone_number=serializer.validated_data["phone_number"]
        )
        # # # # # # # # # # # # # # # # # #
        # send_sms(user.phone_number, otp)
        sms_success, sms_error = True, None
        # # # # # # # # # # # # # # # # # #
        expire_otp = OTP_EXPIRE * 60
        cache.set(f"otp:{user.phone_number}", str(otp))
        cache.expire(f"otp:{user.phone_number}", expire_otp)
        # set otp as user password
        print(f"{otp=}")
        user.set_password(otp)
        user.save()
        # responce based on sms_succes
        if sms_success:
            # success response
            return Response(
                {
                    "ok": True,
                    "phone_number": user.phone_number,
                    "expire": expire_otp,
                },
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data),
            )
        else:
            # fail response
            return Response(
                {
                    "error": "auth-sms",
                    "message": "Failed to send SMS.",
                    "detail": sms_error,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Login(LoginView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        # authenticate user
        user = authenticate(
            phone_number=self.serializer.validated_data["phone_number"],
            password=self.serializer.validated_data["password"],
        )
        if user:
            # generate tokens if auth was successful
            self.user = user
            self.access_token, self.refresh_token = jwt_encode(self.user)
            # TODO: replace 'id' key in responce with user 'UUID' field
            return self.get_response()
        else:
            # fail response
            return Response(
                {
                    "error": "auth-code",
                    "message": "Authentication failed.",
                    "detail": "Phone number or code is not valid.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
