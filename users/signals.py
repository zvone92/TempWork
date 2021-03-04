from django.db.models.signals import post_save
from django.contrib.auth.models import User
from temp.models import Profile


def save_profile(sender, instance, created, **kwargs):
    print('-------------------- if created -------------------')
    if created:
        # this logic to signals
        print('-------------------- try to save-------------------')
        Profile.objects.create(user=instance) # creating user profile
        print('-------------------- USER SAVED   !!! -------------------')


post_save.connect(save_profile, sender=User)
