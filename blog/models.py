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
    ForeignKey,
    DecimalField,
    PositiveBigIntegerField,
)
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation

from comments.models import Comment


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
    title = CharField(max_length=50, unique=True)
    content = TextField(blank=True, null=True)
    slug = SlugField(unique=True, allow_unicode=True, blank=True)
    image = ImageField(blank=True, null=True)
    likes = ManyToManyField(get_user_model(), related_name="article_likes", blank=True)
    bookmarks = ManyToManyField(get_user_model(), related_name="article_bookmarks", blank=True)
    share_qty = BigIntegerField(default=0, blank=True)
    status = IntegerField(choices=status_choices, default=DRAFT)
    original = OneToOneField(
        "self", on_delete=DO_NOTHING, null=True, blank=True, related_name="clone"
    )
    comments = GenericRelation(Comment)
    rate = DecimalField(max_digits=2, decimal_places=1, default=0)
    rate_points = PositiveBigIntegerField(default=0)
    rate_counts = PositiveBigIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title} {int(timezone.now().timestamp())}", allow_unicode=True)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.slug}"
