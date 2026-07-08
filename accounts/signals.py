from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    User create হলে Profile create করবে
    User update হলে Profile ensure করবে
    """

    if created:
        UserProfile.objects.create(user=instance)
        print("Profile created!")

    else:
        UserProfile.objects.get_or_create(user=instance)
        print("Profile ensured/updated!")