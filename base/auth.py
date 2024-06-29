from django.contrib.auth.hashers import check_password
from .models import RegisteredOrg


#used for authenticating when trying to access an admins section, checks password and gives the necessary 
def authenticate_org(email, password):
    try:
        org = RegisteredOrg.objects.get(org_email = email)
        if check_password(password, org.org_password):
            return org
    except RegisteredOrg.DoesNotExist:
        return None

    return org