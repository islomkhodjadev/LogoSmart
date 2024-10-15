from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Parent

@receiver(post_delete, sender=Parent)
def delete_user_on_parent_delete(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
