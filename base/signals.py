## All The Email sending functionality are turned off for now but when connected to the net should be integrated to work properly

from django.conf import settings
from .models import User, Profile, RegisteredOrg, OrgProfile, UserFeedback ,FormSubmissionCounter
from django.db.models.signals import post_save
from django.utils import timezone

#sending email notification
from django.core.mail import send_mail

## for the notify_admin signal ------ 
from django.dispatch import Signal
from django.dispatch import receiver

# admin_added = Signal()

# @receiver(admin_added)
# def notify_new_admin(sender, user, organization, **kwargs):
#     # Send an email to the new admin
#     subject = "You have been added as an Administrator"
#     message = f"Hello {user.username},\n\nYou have been added as an administrator to {organization.org_name}.\n\nBest regards,\nThe Team"
#     send_mail(
#         subject,
#         message,
#         settings.EMAIL_HOST_USER,
#         [user.email],
#         fail_silently=False,
#     )


# when a user registers, it creates a profile and sends the email to the user notifying about their account
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

        # Account Creation and sending emails
        # subject = "Account Creation"
        # message = f"Hello {user.username}, Your Feedlify acount has been successfully created."

        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [user.email],
        #     fail_silently=False
        # )

#when an organization is created, it also creates the profile and sends the email to the user
def createOrgProfile(sender, instance, created, **kwargs):
    if created:
        registered_org = instance
        orgprofile = OrgProfile.objects.create(
            org_name = registered_org,
            org_descr = registered_org.org_descr,
            org_logo = registered_org.org_avatar
        )

        subject = "Feedlify Organization Creation"
        message = f"Welcome {registered_org.org_name} to Feedlify. We hope the feedback system helps improve your organizational perfomance"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, #from
            [registered_org.org_email], #to
            fail_silently= False
        )



# sends to the organization email any time there is a new feedback
def receivedFeedback(sender, instance, created, **kwargs):
    if created:
        org_instance = instance.organization
        print(f"Instance passed is ::: {instance}")

        # Implementing the email notification system    
        counter_obj, created = FormSubmissionCounter.objects.get_or_create(organization=org_instance)
        counter_obj.increment_counter()

        subject = 'There is a New Notification.. 5 feedbacks have been received'
        message = "There is a new message sent to your organizations feedback page"

        if counter_obj.counter >= 5:
            send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, #from
            [org_instance.submited_to], #to
            fail_silently=False,
        )

            counter_obj.reset_counter()
            # Update the last email sent time
            counter_obj.last_email_sent = timezone.now()
            counter_obj.save()


# notification of newly created feedback
post_save.connect(receivedFeedback, sender=UserFeedback)

#notification of creating a profile
post_save.connect(createProfile, sender=User)

#notification of creating an organization profile
post_save.connect(createOrgProfile, sender=RegisteredOrg)