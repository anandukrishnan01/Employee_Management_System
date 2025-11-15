from django.db.models.signals import post_save
from django.dispatch import receiver

from base.functions import get_auto_id
from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={
                'auto_id': get_auto_id(UserProfile),
                'created_by': instance,
            }
        )