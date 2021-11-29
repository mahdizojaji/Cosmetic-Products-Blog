from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from extensions.validators import FutureDateValidator
from comments.models import Comment


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1] or ".jpg"
    # get filename
    if instance.id:
        file_name = f"{int(timezone.now().timestamp())}-{instance.id}.{ext}"
    else:
        # set filename as random string
        file_name = f"{int(timezone.now().timestamp())}-{uuid4().hex}.{ext}"
    # return the whole path to the file
    return f"{instance.content_type.model}/{file_name}"


class MediaFile(models.Model):
    IMAGES = 0
    VIDEOS = 1
    SESSIONS = 2
    FIELD_NAME_CHOICES = (
        (IMAGES, "Images"),
        (VIDEOS, "Videos"),
        (SESSIONS, "Sessions"),
    )
    uuid = models.UUIDField(verbose_name="UUID", unique=True, default=uuid4)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.DO_NOTHING, related_name="media_files")
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ["course", "article"]},
    )
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    file = models.FileField(verbose_name="File", upload_to=path_and_rename)
    field_name = models.IntegerField(verbose_name="Field Name", choices=FIELD_NAME_CHOICES)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

    def __str__(self):
        return f"{self.uuid}"


class Article(models.Model):
    DRAFT = 0
    PENDING = 1
    PUBLISHED = 2
    STATUS_CHOICES = (
        (DRAFT, "Draft"),
        (PENDING, "Pending"),
        (PUBLISHED, "Published"),
    )

    uuid = models.UUIDField(verbose_name="UUID", default=uuid4, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    images = GenericRelation(MediaFile, null=True, blank=True)
    videos = GenericRelation(MediaFile, null=True, blank=True)
    liked_by = models.ManyToManyField(get_user_model(), related_name="users_liked", blank=True)
    bookmarked_by = models.ManyToManyField(get_user_model(), related_name="users_bookmarked", blank=True)
    share_qty = models.BigIntegerField(default=0, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    original = models.OneToOneField("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="clone")
    comments = GenericRelation(Comment, null=True, blank=True)
    premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} {int(timezone.now().timestamp())}", allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"


class Course(models.Model):
    DRAFT = 0
    PENDING = 1
    PUBLISHED = 2
    STATUS_CHOICES = (
        (DRAFT, "Draft"),
        (PENDING, "Pending"),
        (PUBLISHED, "Published"),
    )
    # same fields for online & offline courses:
    uuid = models.UUIDField(verbose_name="UUID", unique=True, default=uuid4)
    author = models.ForeignKey(verbose_name='Author', to=get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(verbose_name='Title', max_length=255)
    slug = models.SlugField(verbose_name='Slug', unique=True, allow_unicode=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    content = models.TextField(verbose_name='Content', null=True, blank=True)
    images = GenericRelation(MediaFile, null=True, blank=True)
    videos = GenericRelation(MediaFile, null=True, blank=True)
    cost = models.PositiveIntegerField(verbose_name='Cost', default=0)
    is_online = models.BooleanField(verbose_name='Is Online')
    quantity = models.PositiveIntegerField(verbose_name='Quantity', validators=[MinValueValidator(1)])
    comments = GenericRelation(Comment, null=True, blank=True)
    rate = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    rate_points = models.PositiveBigIntegerField(default=0)
    rate_counts = models.PositiveBigIntegerField(default=0)
    # online course fields:
    sessions = GenericRelation(MediaFile, null=True, blank=True)
    # offline course fields:
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    deadline = models.DateTimeField(verbose_name='Deadline', null=True, blank=True, validators=[FutureDateValidator()])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} {int(timezone.now().timestamp())}", allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"
