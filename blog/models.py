from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db.models import (
    Model,
    ManyToManyField,
    BigIntegerField,
    IntegerField,
    PositiveIntegerField,
    CharField,
    DateTimeField,
    SlugField,
    TextField,
    ImageField,
    CASCADE,
    SET_NULL,
    DO_NOTHING,
    OneToOneField,
    UUIDField,
    ForeignKey,
    BooleanField,
)
from django.utils.text import slugify
from django.contrib.auth import get_user_model


class MediaFile(Model):
    uuid = UUIDField(verbose_name="UUID", unique=True, default=uuid4)
    object_id = PositiveIntegerField()
    content_type = ForeignKey(ContentType, on_delete=CASCADE, limit_choices_to={'model__in': ['Course']})
    content_object = GenericForeignKey('content_type', 'object_id')
    author = ForeignKey(to=get_user_model(), on_delete=DO_NOTHING, related_name='media_files')


class Article(Model):
    DRAFT = 0
    PENDING = 1
    PUBLISHED = 2
    status_choices = (
        (DRAFT, "Draft"),
        # TODO: Not all fields need to be complete in draft state & it should check in make publish API.
        (PENDING, "Pending"),
        (PUBLISHED, "Published"),
    )

    uuid = UUIDField(verbose_name="UUID", default=uuid4)  # TODO: make all uuid field as unique
    author = ForeignKey(get_user_model(), on_delete=CASCADE)  # TODO: on_delete=SET_NULL
    title = CharField(max_length=50, unique=True)  # TODO: title should not be unique
    content = TextField()
    slug_title = SlugField(unique=True, allow_unicode=True, blank=True)
    image = ImageField()  # TODO: More images & videos should allow but only image can upload with this code.

    likes = ManyToManyField(get_user_model(), related_name="article_likes")
    bookmarks = ManyToManyField(get_user_model(), related_name="article_bookmarks")
    share_qty = BigIntegerField(default=0, blank=True)

    status = IntegerField(choices=status_choices, default=DRAFT)

    original = OneToOneField(
        "self", on_delete=DO_NOTHING, null=True, blank=True, related_name="clone"
    )

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug_title

    def save(self, *args, **kwargs):
        """Slugify the title before save."""
        self.slug_title = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)


class Course(Model):
    DRAFT = 0
    PENDING = 1
    PUBLISHED = 2
    status_choices = (
        (DRAFT, "Draft"),
        (PENDING, "Pending"),
        (PUBLISHED, "Published"),
    )
    # same fields for online & offline courses:
    uuid = UUIDField(verbose_name="UUID", unique=True, default=uuid4)
    author = ForeignKey(verbose_name='Author', to=get_user_model(), on_delete=SET_NULL, null=True)
    title = CharField(verbose_name='Title', max_length=255)
    slug = SlugField(verbose_name='Slug', unique=True, allow_unicode=True, blank=True)
    status = IntegerField(choices=status_choices, default=DRAFT)
    content = TextField(verbose_name='Content', null=True, blank=True)
    images = GenericRelation(MediaFile)
    videos = GenericRelation(MediaFile)
    cost = PositiveIntegerField(verbose_name='Cost', default=0)
    is_online = BooleanField(verbose_name='Is Online')
    quantity = PositiveIntegerField(verbose_name='Quantity', validators=[MinValueValidator(1)])
    # online course fields:
    sessions = GenericRelation(MediaFile)
    # offline course fields:
    address = TextField(verbose_name='Address', null=True, blank=True)
    deadline = DateTimeField(verbose_name='Deadline', null=True, blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug}"
