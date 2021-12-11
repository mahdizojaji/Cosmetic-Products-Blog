from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from blog.models import Course, Article

from .models import Comment


def apply_rate(obj: Article or Course, value: int, unset: bool = False):
    """Calculate rate for object based on UNSET argument

    Args:
        obj (Model): object to calculate rate for
        value (int): value to add to rate_points
        unset (bool, optional): flag for removing previous rate. Defaults to False.
    """
    if unset:
        obj.rate_counts -= 1
        obj.rate_points -= value
        # author
        obj.author.rate_counts -= 1
        obj.author.rate_points -= value
    else:
        obj.rate_counts += 1
        obj.rate_points += value
        # author
        obj.author.rate_counts += 1
        obj.author.rate_points += value

    if obj.rate_counts > 0:
        obj.rate = obj.rate_points / obj.rate_counts
    else:
        obj.rate = 0
    # author
    if obj.author.rate_counts > 0:
        obj.author.rate = obj.author.rate_points / obj.author.rate_counts
    else:
        obj.author.rate = 0


@receiver(pre_save, sender=Comment)
def comment_pre_save(sender, instance, **kwargs):
    obj = instance.content_object
    if not instance.rate:
        # if object is not rateable or if rate is not set,
        # we don't need to do anything.
        return
    org = Comment.objects.filter(uuid=instance.uuid)
    if org.exists():
        org = org.first()
        # if comment was updated first we need to remove previous rate ->
        apply_rate(obj, org.rate, True)
    # adding rate to object and save it ->
    apply_rate(obj, instance.rate)
    obj.save()
    obj.author.comment_qty += 1
    obj.author.save()


@receiver(pre_delete, sender=Comment)
def comment_pre_delete(sender, instance, **kwargs):
    obj = instance.content_object
    if not instance.rate:
        # if object is not rateable or if rate is not set,
        # we don't need to do anything.
        return
    # adding rate to object and save it ->
    apply_rate(obj, instance.rate, True)
    obj.save()
    obj.author.comment_qty -= 1
    obj.author.save()
