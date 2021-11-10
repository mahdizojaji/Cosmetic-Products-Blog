from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Comment


@receiver(post_save, sender=Comment)
def apply_rate(sender, instance, created, **kwargs):
    if created:
        obj = instance.content_object
        obj.rate_counts += 1
        obj.rate_points += instance.rate
        obj.rate = obj.rate_points / obj.rate_counts
        obj.save()
        # or obj.apply_rate() method can be used ->
        #   obj.apply_rate(instance.rate)


@receiver(post_delete, sender=Comment)
def clear_rate(sender, instance, **kwargs):
    obj = instance.content_object
    obj.rate_counts -= 1
    obj.rate_points -= instance.rate
    obj.rate = obj.rate_points / obj.rate_counts
    obj.save()
