from django.shortcuts import render, redirect
from . forms import MyUserCreationForm, OrgForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import RegisteredOrg, User,Profile, UserFeedback, FeedbackType
from .auth import authenticate_org
from django.db.models import Q
from django.contrib.auth.decorators import login_required

#### ------- Home, Login, Logout, Signup------  ####
def home(request):
    return render(request, 'base/home.html')

def signup_user(request):
    page = 'signup'

    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form':form, 'page':page}
    return render(request, 'base/signup_login.html', context)

def login_user(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # email = request.POST.get('email').lower()
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'base/signup_login.html')
def logout_user(request):
    logout(request)
    return redirect('home')


#### ------- Register Company ------  ####
@login_required(login_url='login')
def register_company(request):
    page = 'register-company'
    form = OrgForm()
    if request.method == 'POST':
        form = OrgForm(request.POST)
        if form.is_valid():
            org_form = form.save(commit=False)
            org_form.super_admin = request.user
            # user = User.objects.get(email = user_email)
            # org_form.org_admins.add(request.user)

            org_form.save()
            org_form.org_admins.add(request.user)

            return redirect('home')

    context = {'form':form, 'page':page}
    return render(request, 'base/login_ad_register.html', context)

@login_required(login_url='login')
def login_admin(request):
    page = 'login_admin'
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('org_email')
        password = request.POST.get('org_password')
        try:
            organization = RegisteredOrg.objects.get(org_email=email)
            org = authenticate_org(email=email, password=password)

            # if request.user.email in organization.org_admins or request.user == organization.super_admin:
            #     org = authenticate_org(email=email, password=password)
            # else:
            #     org = None
        except:
            messages.error(request, 'There Was an Error trying to access the admins page')
            org = None
        ## the authenticate is designed to work only with the user model and cant work with a different
        
        #in the below line, there will also be an option to check if the request.user is in org.org_admins
        if org is not None :
           
            return redirect('admins_page', pk=org.id)
        # else:
        #     messages.error(request, 'There Was an Error trying to access the admins page')
    context = {'page':page}


    return render(request, 'base/login_ad_register.html', context)


@login_required(login_url='login')
def admins_page(request, pk):
    feedback_categories = FeedbackType.objects.all()
    organization = RegisteredOrg.objects.get(id=pk)

    # implementing functionality to return the feedbacks based on the feedbck type

    q = request.GET.get('q', '')  # Get the query parameter 'q' or use an empty string if not provided

    # Filter feedbacks by the organization and the feedback type
    org_feedbacks = UserFeedback.objects.filter(
        organization=organization,
        feedback_type__name__icontains=q  # Use __icontains for case-insensitive matching
    )

    # org_feedbacks = organization.userfeedback_set.all()
    if not request.user.is_authenticated:
        return redirect('home')
    
    context = {'organization':organization, 'org_feedbacks':org_feedbacks, 'feedback_categories':feedback_categories}
    return render(request, 'base/admins.html', context)

@login_required(login_url='login')
def user_profile(request, pk):
    page = 'user_profile'
    user = User.objects.get(id=pk)
    form = ProfileForm()

    context = {'form':form, 'user':user, 'page':page}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def update_profile(request, pk):
    page = 'update_user_profile'
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    context = {'form':form, 'page':page}
    return render(request, 'base/update_form.html', context)

def delete_profile(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        user.delete()
        return  redirect('home')
    context = {'obj':user}
    return render(request, 'base/delete.html', context)

def appreciation_page(request):
    page = 'appreciation_page'
    context = {'page':page}
    return render(request, 'base/site_basics.html', context)