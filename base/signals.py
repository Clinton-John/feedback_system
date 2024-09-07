from django.conf import settings
from .models import User, Profile, RegisteredOrg, OrgProfile, UserFeedback
from django.db.models.signals import post_save

#sending email notification
from django.core.mail import send_mail

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
        orgprofile = OrgProfile.objects.create(
            org_name = registered_org,
            org_descr = registered_org.org_descr,
            org_logo = registered_org.org_avatar
        )



# sends to the organization email any time there is a new feedback
def receivedFeedback(sender, instance, created, **kwargs):
    if created:
        org_instance = instance
        subject = 'There is a New Notification'
        message = "There is a new message sent to your organizations feedback page"

        send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER, #from
        [org_instance.submited_to], #to
        fail_silently=False,
    )



post_save.connect(receivedFeedback, sender=UserFeedback)
post_save.connect(createProfile, sender=User)
post_save.connect(createOrgProfile, sender=RegisteredOrg)