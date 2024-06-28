from django.contrib.auth.forms import UserCreationForm
from .models import User, RegisteredOrg
from django.forms import ModelForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username','first_name','last_name','email' , 'password1', 'password2']

    

class OrgForm(ModelForm):
    class Meta:
        model = RegisteredOrg
        fields = ['org_name','org_email','org_descr']