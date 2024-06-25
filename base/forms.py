from django.contrib.auth.forms import UserCreationForm
from .models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # fields = '__all__'
        # exclude = []
        fields = [ 'username','first_name','last_name','email' , 'password1', 'password2']

    
