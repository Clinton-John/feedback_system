from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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