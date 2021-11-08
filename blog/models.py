from uuid import uuid4

from django.db.models import (
    Model,
    ManyToManyField,
    BigIntegerField,
    IntegerField,
    CharField,
    DateTimeField,
    SlugField,
    TextField,
    ImageField,
    CASCADE,
    DO_NOTHING,
    OneToOneField,
    UUIDField,
    ForeignKey
)
from django.utils.text import slugify
from django.contrib.auth import get_user_model


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
