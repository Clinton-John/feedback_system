from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(unique=True, null=True)
    about_you = models.TextField(null=True)
    profile_pic = models.ImageField(null=True , blank=True, default="avatar.svg") #later add the default profile image
    # profile_pic = models.ImageField(default="avatar.svg", null=True , blank=True)

    def  __str__(self):
        return self.username

class RegisteredOrg(models.Model):
    org_name = models.CharField(null=True, max_length=100)
    org_email = models.EmailField(null=True, max_length=100)
    org_qr_code = models.ImageField(null=True, blank=True)
    org_avatar = models.ImageField(null=True , blank=True)
    org_descr = models.TextField(null=True)
    super_admin =  models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='super_admin_organizations')
    org_admins = models.ManyToManyField(User, related_name='admin_organizations')
    org_password = models.CharField(max_length=128, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.org_name

# The profile contains the customer care information that will be added to the  scanned page
class OrgProfile(models.Model):
    org_name = models.OneToOneField(RegisteredOrg, on_delete=models.CASCADE)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    org_address = models.TextField(null=True, blank=True)
    # org_description = models.TextField(null=True, blank=True)
    org_descr = models.TextField(null=True)
    org_logo = models.ImageField(null=True, blank=True)
    org_website = models.URLField(null=True, blank=True)
    org_facebook = models.URLField(null=True, blank=True)
    org_twitter = models.URLField(null=True, blank=True)
    org_instagram = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.org_name.org_name

## v 1.0
class FeedbackType(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self) :
        return self.name

class UserFeedback(models.Model):
    organization = models.ForeignKey(RegisteredOrg, on_delete=models.CASCADE, null=True)
    user_email = models.EmailField(max_length=200, null=True, blank=True)
    # feedback_type = models.CharField(max_length=100, null=True, blank=True)
    ##v 1.0
    feedback_type = models.ForeignKey(FeedbackType, on_delete=models.CASCADE, null=True, blank=True)

    user_feedback = models.TextField()
    user_ratings = models.IntegerField(null=True, blank=True)
    submited_to = models.EmailField(max_length=100, null=True, blank=True)
    submit_date = models.DateTimeField(auto_now_add=True)

    #to handle the reply functionality 
    admin_response = models.TextField(null=True, blank=True)
    response_sent = models.BooleanField(default=False) 

    def __str__(self):
        return self.user_feedback

# Implementing the customized notification 
class FormSubmissionCounter(models.Model):
    organization = models.OneToOneField(RegisteredOrg, on_delete=models.CASCADE, related_name='submission_counter')
    # organization = models.OneToOneField(RegisteredOrg, on_delete=models.CASCADE, related_name='submission_counter', default=1)
    counter = models.IntegerField(default=0)
    last_email_sent = models.DateTimeField(null=True, blank=True)

    def increment_counter(self):
        self.counter += 1
        self.save()

    def reset_counter(self):
        self.counter = 0
        self.save()

class NotificationSettings(models.Model):
    organization = models.OneToOneField(RegisteredOrg, on_delete=models.CASCADE)
    notification_status = models.TextField(null=True, blank=True, default='On')
    no_of_notifications = models.IntegerField(default=1)

    def __str__(self):
        return self.notification_status
