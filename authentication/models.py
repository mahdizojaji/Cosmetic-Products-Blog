import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db.models import CharField, UUIDField, EmailField
from django.db.models.fields import BigIntegerField, BooleanField, DateTimeField


class UserManager(BaseUserManager):
    def create_user(
        self,
        phone_number,
        password,
        is_staff=False,
        is_superuser=False,
        is_active=True,
        **extra_fields
    ):
        if not phone_number:
            raise ValueError("Users must have a phone_number")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            phone_number=phone_number,
            **extra_fields,
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uuid = UUIDField(verbose_name="UUID", default=uuid.uuid4)

    phone_number_validator = RegexValidator(
        regex=r"^\+989\d{9}$", message="Phone number must be entered."
    )

    phone_number = CharField(
        validators=[phone_number_validator],
        max_length=13,
        null=False,
        blank=False,
        unique=True,
    )

    email = EmailField(null=True,blank=True)

    code_expire = BigIntegerField(default=0,blank=True)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return self.phone_number

    def get_short_name(self):
        return self.phone_number
