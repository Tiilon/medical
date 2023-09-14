from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from health.models import Patient
from .models import UserProfile
from djoser.signals import user_activated

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when a new user is created.
    """
    if created:
        print(f"User created: {instance.email}")
        UserProfile.objects.create(user=instance)
