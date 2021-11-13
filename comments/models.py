from uuid import uuid4
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    PositiveIntegerField,
    UUIDField,
    CASCADE,
    DateTimeField,
    SmallIntegerField,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


class Comment(Model):
    uuid = UUIDField(verbose_name="UUID", default=uuid4, unique=True)
    text = CharField(max_length=100)
    author = ForeignKey(get_user_model(), on_delete=CASCADE, related_name="comments")
    rate = SmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], blank=True, null=True
    )
    created_at = DateTimeField(auto_now_add=True)

    content_type = ForeignKey(
        ContentType, limit_choices_to={"model__in": ["article"]}, on_delete=CASCADE
    )
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
