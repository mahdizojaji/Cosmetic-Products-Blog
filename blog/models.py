from uuid import uuid4

from django.db.models import (
    Model,
    ManyToManyField,
    BigIntegerField,
    CharField,
    DateTimeField,
    SlugField,
    TextField,
    ImageField,
    CASCADE
)
from django.db.models.fields import UUIDField
from django.db.models.fields.related import ForeignKey
from django.utils.text import slugify
from django.contrib.auth import get_user_model



class Article(Model):
    uuid = UUIDField(verbose_name="UUID", default=uuid4)
    author = ForeignKey(get_user_model(), on_delete=CASCADE)
    title = CharField(max_length=50, unique=True)
    content = TextField()
    slug_title = SlugField(unique=True, allow_unicode=True)
    image = ImageField()

    likes = ManyToManyField(get_user_model(), related_name="article_likes")
    bookmarks = ManyToManyField(get_user_model(), related_name="article_bookmarks")
    share_qty = BigIntegerField(default=0, blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug_title

    def save(self, *args, **kwargs):
        """Slugify the title before save."""
        self.slug_title = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)
