import uuid

from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db.models import (
    CharField,
    UUIDField,
    EmailField,
    BigIntegerField,
    BooleanField,
    DateField,
    DateTimeField,
    ImageField,
    ManyToManyField,
    DecimalField,
    PositiveBigIntegerField,
)
from django.db.models.fields import IntegerField

from config.settings import PHONE_NUMBER_PATTERN


class UserManager(BaseUserManager):
    def create_user(
        self,
        phone_number,
        password,
        is_staff=False,
        is_superuser=False,
        is_active=True,
        **extra_fields,
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


iran_provinces = (
    (1, "آذربایجان شرقی"),
    (2, "آذربایجان غربی"),
    (3, "اردبیل"),
    (4, "اصفهان"),
    (5, "البرز"),
    (6, "ایلام"),
    (7, "بوشهر"),
    (8, "تهران"),
    (9, "چهارمحال و بختیاری"),
    (10, "خراسان جنوبی"),
    (11, "خراسان رضوی"),
    (12, "خراسان شمالی"),
    (13, "خوزستان"),
    (14, "زنجان"),
    (15, "سمنان"),
    (16, "سیستان و بلوچستان"),
    (17, "فارس"),
    (18, "قزوین"),
    (19, "قم"),
    (20, "کردستان"),
    (21, "کرمان"),
    (22, "کرمانشاه"),
    (23, "کهگیلویه و بویراحمد"),
    (24, "گلستان"),
    (25, "لرستان"),
    (26, "گیلان"),
    (27, "مازندران"),
    (28, "مرکزی"),
    (29, "هرمزگان"),
    (30, "همدان"),
    (31, "یزد"),
)


class User(AbstractBaseUser, PermissionsMixin):
    uuid = UUIDField(verbose_name="UUID", default=uuid.uuid4, unique=True)
    phone_number_validator = RegexValidator(
        regex=PHONE_NUMBER_PATTERN, message="Phone number must be entered."
    )

    phone_number = CharField(
        validators=[phone_number_validator],
        max_length=13,
        null=False,
        blank=False,
        unique=True,
    )
    code_expire = BigIntegerField(default=0, blank=True)
    email = EmailField(null=True, blank=True)
    birth_date = DateField(null=True, blank=True)
    fname = CharField(max_length=30, null=True, blank=True)
    lname = CharField(max_length=30, null=True, blank=True)
    job_title = CharField(max_length=30, null=True, blank=True)
    bio = CharField(max_length=80, null=True, blank=True)
    avatar_img = ImageField(
        upload_to="users/avatars/",
        height_field=None,
        width_field=None,
        null=True,
        blank=True,
    )
    cover_img = ImageField(
        upload_to="users/covers/",
        height_field=None,
        width_field=None,
        null=True,
        blank=True,
    )
    province = IntegerField(choices=iran_provinces, blank=True, null=True)
    city = CharField(max_length=30, blank=True, null=True)
    subscription_expire = BigIntegerField(default=0, blank=True)
    liked_by = ManyToManyField("self", related_name="liked_users", blank=True)
    bookmarked_by = ManyToManyField("self", related_name="bookmarked_users", blank=True)
    share_qty = BigIntegerField(default=0, blank=True)
    comment_qty = BigIntegerField(default=0, blank=True)
    rate = DecimalField(max_digits=2, decimal_places=1, default=0)
    rate_points = PositiveBigIntegerField(default=0)
    rate_counts = PositiveBigIntegerField(default=0)
    credit = PositiveBigIntegerField(default=0)
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

    def name(self):
        return f"{self.fname} {self.lname}"

    def reverse_url(self):
        return reverse("users:user_retrieve", kwargs={"uuid": self.uuid})
