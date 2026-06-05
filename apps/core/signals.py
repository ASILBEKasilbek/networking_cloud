from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.models import CustomUser, NotificationPreference


@receiver(post_save, sender=CustomUser)
def create_notification_preference(sender, instance, created, **kwargs):
    """Create notification preference when user is created."""
    if created:
        NotificationPreference.objects.get_or_create(user=instance)
