from .models import User, Profile, RegisteredOrg, OrgProfile
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

def createOrgProfile(sender, instance, created, **kwargs):
    if created:
        registered_org = instance
        profile = OrgProfile.objects.create(
            org_name = registered_org.org_name,
            org_description = registered_org.org_descr,
            org_logo = registered_org.org_avatar
        )

post_save.connect(createProfile, sender=User)
post_save.connect(createOrgProfile, sender=RegisteredOrg)