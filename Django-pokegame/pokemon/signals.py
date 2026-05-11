from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_player_for_user(sender, instance, created, **kwargs):
    """Automatically create a linked Player whenever a new User is saved."""
    if created:
        from .models import Player
        Player.objects.get_or_create(user=instance, defaults={'name': instance.username})