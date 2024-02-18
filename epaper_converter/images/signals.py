from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from .models import Image

@receiver(post_delete, sender=Image)
def on_image_delete(sender, instance, **kwargs):
    instance.original_image.delete(False)
    instance.converted_image.delete(False)
    instance.thumbnail.delete(False)