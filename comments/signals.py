from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Comment


@receiver(post_save, sender=Comment)
def apply_rate(sender, instance, created, **kwargs):
    if created:
        instance.content_object.rate_counts += 1
        instance.content_object.rate_points += instance.rate
        instance.content_object.rate = (
            instance.content_object.rate_points / instance.content_object.rate_counts
        )
        instance.content_object.save()
        # or instance.content_object.apply_rate() method can be used ->
        #   instance.content_object.apply_rate(instance.rate)
