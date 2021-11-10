from django.db.models.base import Model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

from .models import Comment
from config.settings import RATE_MODELS


def set_rate(obj: Model, value: int):
    obj.rate_counts += 1
    obj.rate_points += value
    obj.rate = obj.rate_points / obj.rate_counts


def unset_rate(obj: Model, value: int):
    obj.rate_counts -= 1
    obj.rate_points -= value
    obj.rate = obj.rate_points / obj.rate_counts


@receiver(pre_save, sender=Comment)
def apply_rate(sender, instance, created=False, **kwargs):
    obj = instance.content_object
    if obj._meta.model_name not in RATE_MODELS:
        return

    if not created:
        org = Comment.objects.get(uuid=instance.uuid)
        unset_rate(obj, org.rate)

    set_rate(obj, instance.rate)
    obj.save()
    # print("old:",org.rate)
    # print("new:",instance.rate)


@receiver(post_delete, sender=Comment)
def clear_rate(sender, instance, **kwargs):
    obj = instance.content_object
    if obj._meta.model_name not in RATE_MODELS:
        return

    unset_rate(obj, instance.rate)
    obj.save()
