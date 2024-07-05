from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RegisteredOrg

def admins_dashboard(request):
    if 'org_id' in request.session:
        org_id = request.session['org_id']
        try:
            org = RegisteredOrg.objects.get(id=org_id)
            return render(request, 'admins_dashboard.html', {'org': org})
        except RegisteredOrg.DoesNotExist:
            messages.error(request, 'Organization not found')
    else:
        messages.error(request, 'Please log in')

    return redirect('login_admin') 



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RegisteredOrg
from .auth import authenticate_org  # Import your custom authentication function

def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('org_email')
        password = request.POST.get('org_password')

        try:
            org = RegisteredOrg.objects.get(org_email=email)
        except RegisteredOrg.DoesNotExist:
            messages.error(request, 'No organization registered using the email')
            return render(request, 'base/login_admin.html')

        org = authenticate_org(email=email, password=password)

        if org is not None:
            # Store organization ID in session
            request.session['org_id'] = org.id
            return redirect('admins_dashboard')  # Redirect to admins dashboard
        else:
            messages.error(request, 'There was an error during login')

    return render(request, 'base/login_admin.html')
