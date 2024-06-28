from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class RegisteredOrg(models.Model):
    org_name = models.CharField(null=True, max_length=100)
    org_email = models.EmailField(null=True, max_length=100)
    org_descr = models.TextField(null=True)
    org_admin =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # org_avatar = 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __self__(self):
        return self.org_name