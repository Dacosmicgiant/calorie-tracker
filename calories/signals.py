# calories/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile when a new User is created, or ensure it exists
    """
    if created:
        # User was just created, create profile
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'daily_calorie_goal': 2000}
        )
    else:
        # User was updated, ensure profile exists
        if not hasattr(instance, 'userprofile'):
            UserProfile.objects.get_or_create(
                user=instance,
                defaults={'daily_calorie_goal': 2000}
            )