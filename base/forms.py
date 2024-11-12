from django.contrib.auth.forms import UserCreationForm
from .models import User, RegisteredOrg, UserFeedback, Profile, OrgProfile
from django.forms import ModelForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username','first_name','last_name','email' , 'password1', 'password2']


class OrgForm(ModelForm):
    class Meta:
        model = RegisteredOrg
        fields = ['org_name','org_email', 'org_avatar', 'org_password' ,'org_descr']

class UpdateOrgForm(ModelForm):
    class Meta:
        model = RegisteredOrg
        fields = ['org_name', 'org_avatar' ,'org_descr']


class OrgUpdateForm(ModelForm):
    class Meta:
        model = OrgProfile
        fields = '__all__'
        exclude = ['org_name']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class AdminResponseForm(ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['admin_response']
        # widgets = {
        #     'admin_response': format.Textarea(attrs={'placeholder': 'Write your response here...', 'rows': 4}),
        # }
