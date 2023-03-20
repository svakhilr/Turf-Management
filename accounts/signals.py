from django.db.models.signals import post_save, pre_delete
from .models import Accounts
from django.dispatch import receiver
from .models import UserProfile,VendorProfile
# from vendor.models import VendorProfile


@receiver(post_save, sender=Accounts)
def create_profile(sender, instance, created, **kwargs):
    print("triggered")
    if not created and instance.role == 'CUSTOMER':

        UserProfile.objects.get_or_create(user=instance)

    elif not created and instance.role == 'VENDOR':
        print("vendortriggered")
        VendorProfile.objects.get_or_create(user=instance)

