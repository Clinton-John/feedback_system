from django.shortcuts import render, redirect
from . forms import MyUserCreationForm, OrgForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import RegisteredOrg, User,Profile, UserFeedback
from .auth import authenticate_org



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
def register_company(request):
    page = 'register-company'
    form = OrgForm()
    if request.method == 'POST':
        form = OrgForm(request.POST)
        if form.is_valid():
            org_form = form.save(commit=False)
            org_form.save()
            org_form.org_admins.add(request.user)
            # org_form.org_admins = request.user
            return redirect('home')

    context = {'form':form, 'page':page}
    return render(request, 'base/login_ad_register.html', context)

def login_admin(request):
    page = 'login_admin'
    if request.method == 'POST':
        email = request.POST.get('org_email')
        password = request.POST.get('org_password')

        try:
            org = RegisteredOrg.objects.get(org_email=email)
        except:
            messages.error(request, 'No Organization registered using the email')
        
        ## the authenticate is designed to work only with the user model and cant work with a different
        org = authenticate_org(email=email, password=password)
        
        #in the below line, there will also be an option to check if the request.user is in org.org_admins
        if org is not None :
            # access the organization id which will be passed together with the link in the redirect for a specifc page

            return redirect('admins_page', pk=org.id)
        else:
            messages.error(request, 'There Was an Error during Login')
    context = {'page':page}


    return render(request, 'base/login_ad_register.html', context)

def admins_page(request, pk):
    feedback_list = ['Complaint', 'Suggestion','Praise', 'Question']

    feedback_list2 = {
        'complaint': 'Complaint',
        'suggestion': 'Suggestion',
        'praise': 'Praise',
        'question': 'Question'

    }
        
    organization = RegisteredOrg.objects.get(id=pk)
    org_feedbacks = organization.userfeedback_set.all()
    if not request.user.is_authenticated:
        return redirect('home')
    
    context = {'organization':organization, 'org_feedbacks':org_feedbacks, 'feedback_list':feedback_list}
    return render(request, 'base/admins.html', context)


def user_profile(request, pk):
    page = 'user_profile'
    user = User.objects.get(id=pk)
    form = ProfileForm()

    context = {'form':form, 'user':user, 'page':page}
    return render(request, 'base/profile.html', context)

def update_profile(request, pk):
    page = 'update_user_profile'
    user = request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    context = {'form':form, 'page':page}
    return render(request, 'base/update_form.html', context)

def appreciation_page(request):
    return render(request, 'base/appreciation.html')