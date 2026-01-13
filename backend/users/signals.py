from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a CustomUser is created."""
    if created:
        # Use get_or_create to avoid duplicate profile creation
        UserProfile.objects.get_or_create(user=instance)
