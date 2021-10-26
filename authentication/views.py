from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from config.settings import OTP_EXPIRE, SMS
from rest_framework.response import Response
from dj_rest_auth.views import LoginView, UserDetailsView
from dj_rest_auth.utils import jwt_encode
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from .permissions import OwnerAndAdmin, OwnerAndAdminOrReadOnly
from .serializers import (
    SendCodeSerializer,
    LoginSerializer,
    UserDetailsSerializer,
    UserProfileFullSerializer,
    UserProfileLimitedSerializer,
)
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
        # set code expire time
        user.code_expire = int(timezone.now().timestamp()) + expire_otp
        # set otp as user password
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

    def login(self):
        self.access_token, self.refresh_token = jwt_encode(self.user)
        self.process_login()

    def post(self, request, *args, **kwargs):
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
                # TODO: replace 'id' key in responce with user 'UUID' field
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


class UserDetails(UserDetailsView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]


class UserProfile(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = "uuid"

    def get_serializer_class(self):
        if OwnerAndAdmin().has_object_permission(
            request=self.request, view=self, obj=self.get_object()
        ):
            return UserProfileFullSerializer

        return UserProfileLimitedSerializer


class UserLike(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user = request.user
        if user in user_profile.liked_by.all():
            user_profile.liked_by.remove(user)
        else:
            user_profile.liked_by.add(user)
        return Response(status=status.HTTP_200_OK)


class UserBookmark(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "uuid"

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user = request.user
        if user in user_profile.bookmarked_by.all():
            user_profile.bookmarked_by.remove(user)
        else:
            user_profile.bookmarked_by.add(user)
        return Response(status=status.HTTP_200_OK)
