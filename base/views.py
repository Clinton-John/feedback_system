from django.shortcuts import render, redirect
from . forms import MyUserCreationForm, OrgForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



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
    form = OrgForm()
    if request.method == 'POST':
        form = OrgForm(request.POST)
        if form.is_valid():
            org_form = form.save(commit=False)
            org_form.org_admin = request.user
            org_form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/register_comp.html', context)

