from uuid import uuid4
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


class Comment(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid4, unique=True)
    text = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    rate = models.SmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType, limit_choices_to={"model__in": ["article"]}, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
