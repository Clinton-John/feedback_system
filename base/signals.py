from .models import User, Profile
from django.db.models.signals import post_save

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username= user.username,
            first_name= user.first_name,
            last_name=user.last_name,
            email = user.email

        )

post_save.connect(createProfile, sender=User)