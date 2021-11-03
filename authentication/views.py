from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from dj_rest_auth.utils import jwt_encode

from .serializers import SendCodeSerializer, LoginSerializer
from extensions.sms import generate_random_code, send_otp_sms
from config import settings

User = get_user_model()


class SendCodeAPIView(CreateAPIView):
    serializer_class = SendCodeSerializer

    def create(self, request, *args, **kwargs):
        # validating serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # get or create user
        user, _ = User.objects.get_or_create(
            phone_number=serializer.validated_data["phone_number"]
        )
        if settings.SMS["DEBUG_MODE"]:
            otp = "123456"
            sms_success, sms_error = True, None
        else:
            # generating random code
            otp = f"{generate_random_code()}"
            sms_response = send_otp_sms(user.phone_number, otp).json()
            sms_success = (
                True if sms_response.get("result", {}).get("code") == 200 else False
            )
            sms_error = (
                None if sms_success else sms_response.get("result", {}).get("message")
            )
        # set code expire time
        user.code_expire = int(timezone.now().timestamp() + (settings.OTP_EXPIRE * 60))
        # set otp as user password
        user.set_password(otp)
        user.save()
        # response based on sms success
        if sms_success:
            # success response
            return Response(
                {
                    "ok": True,
                    "phone_number": user.phone_number,
                    "expire": user.code_expire,
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


class LoginAPIView(LoginView):
    refresh_token: str
    request: Request
    serializer: serializers.Serializer
    serializer_class = LoginSerializer

    def login(self):
        self.access_token, self.refresh_token = jwt_encode(self.user)
        self.process_login()

    def post(self, request: Request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        phone = self.serializer.validated_data["phone_number"]
        code = self.serializer.validated_data["password"]
        # authenticate user
        user = authenticate(
            phone_number=phone,
            password=code,
        )
        if user:
            # checking code expire time
            if user.code_expire > int(timezone.now().timestamp()):
                self.user = user
                self.login()
                # THE HAPPY ENDING ~>
                return self.get_response()
            else:
                response = {
                    "error": "auth-expire",
                    "message": "Authentication failed.",
                    "detail": "Login code expired.",
                }
        else:
            response = {
                "error": "auth-code",
                "message": "Authentication failed.",
                "detail": "Phone number or code is not valid.",
            }
        return Response(
            response,
            status=status.HTTP_401_UNAUTHORIZED,
        )
