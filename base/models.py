from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    about_you = models.TextField(null=True)
    profile_pic = models.ImageField(null=True , blank=True) #later add the default profile image
    # profile_pic = models.ImageField(default="avatar.svg", null=True , blank=True)

    def  __str__(self):
        return self.username


class RegisteredOrg(models.Model):
    org_name = models.CharField(null=True, max_length=100)
    org_email = models.EmailField(null=True, max_length=100)
    org_descr = models.TextField(null=True)
    org_admins = models.ManyToManyField(User, related_name='admin_organizations')
    org_password = models.CharField(max_length=128, null=True)
    # org_avatar = 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.org_name

class UserFeedback(models.Model):
    # organization = models.ForeignKey(RegisteredOrg, on_delete=models.CASCADE, null=True)
    user_email = models.EmailField(max_length=200, null=True, blank=True)
    feedback_type = models.CharField(max_length=100, null=True, blank=True)
    user_feedback = models.TextField()
    user_ratings = models.IntegerField(null=True, blank=True)
    submit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_feedback