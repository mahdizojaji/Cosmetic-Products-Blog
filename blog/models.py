from uuid import uuid4
from django.db import models
from django.db.models import (
    Model,
    ManyToManyField,
    BigIntegerField,
    IntegerField,
    CharField,
    DateTimeField,
    SlugField,
    TextField,
    CASCADE,
    DO_NOTHING,
    OneToOneField,
    UUIDField,
    ForeignKey,
    DecimalField,
    PositiveBigIntegerField,
)
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from comments.models import Comment


def path_and_rename(instance, filename):
    ext = filename.split(".")[-1] or ".jpg"
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
    author = models.ForeignKey(
        to=get_user_model(), on_delete=models.DO_NOTHING, related_name="media_files"
    )
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ["course", "article"]},
    )
    content_object = GenericForeignKey("content_type", "object_id")
    file = models.FileField(verbose_name="File", upload_to=path_and_rename)
    field_name = models.IntegerField(verbose_name="Field Name", choices=FIELD_NAME_CHOICES)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

    def __str__(self):
        return f"{self.uuid}"


class Article(Model):
    DRAFT = 0
    PENDING = 1
    PUBLISHED = 2
    status_choices = (
        (DRAFT, "Draft"),
        (PENDING, "Pending"),
        (PUBLISHED, "Published"),
    )

    uuid = UUIDField(verbose_name="UUID", default=uuid4, unique=True)
    author = ForeignKey(get_user_model(), on_delete=CASCADE)
    title = CharField(max_length=50)
    content = TextField(blank=True, null=True)
    slug = SlugField(unique=True, allow_unicode=True, blank=True)
    images = GenericRelation(MediaFile, null=True, blank=True)
    videos = GenericRelation(MediaFile, null=True, blank=True)
    likes = ManyToManyField(get_user_model(), related_name="article_likes", blank=True)
    bookmarks = ManyToManyField(
        get_user_model(), related_name="article_bookmarks", blank=True
    )
    share_qty = BigIntegerField(default=0, blank=True)
    status = IntegerField(choices=status_choices, default=DRAFT)
    original = OneToOneField(
        "self", on_delete=DO_NOTHING, null=True, blank=True, related_name="clone"
    )
    comments = GenericRelation(Comment, null=True, blank=True)
    rate = DecimalField(max_digits=2, decimal_places=1, default=0)
    rate_points = PositiveBigIntegerField(default=0)
    rate_counts = PositiveBigIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(
            f"{self.title} {int(timezone.now().timestamp())}", allow_unicode=True
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"
