'''
views_admin
  --> generate qrcode /  generate new qrcode
  --> add company questions
  --> add administrators -- Done
  --> upgrade administrators
  --> remove administrators --Done
  --> get stored qr code
'''

from .models import RegisteredOrg, User, UserFeedback
from django.contrib import messages
from .forms import OrgForm, UpdateOrgForm

from django.shortcuts import render, redirect
from .models import UserFeedback, RegisteredOrg

def feedback_page(request):
  if request.method == 'POST':

    user_email = request.POST.get('user_email')

    feedback = UserFeedback.objects.create(
      user_email = request.POST.get('user_email'),
      feedback_type = request.POST.get('feedback_type'),
      user_feedback = request.POST.get('user_feedback'),
      user_ratings =request.POST.get('user_ratings')
    )
    return redirect('home')


  return render(request, 'base/qrcode_form.html')

def add_admin(request, pk):
  page = 'add_admin'

  if not request.user.is_authenticated:
    return redirect('home')


  r_organization = RegisteredOrg.objects.get(id=pk)

  if request.method == 'POST':
    user_email = request.POST.get('email')
    registered_users = User.objects.all()
    
    if registered_users.filter(email=user_email).exists():
      user = User.objects.get(email = user_email)
      r_organization.org_admins.add(user)
      messages.success(request,f"{user.username} Successfully added as an administrator to {r_organization.org_name}")

      return redirect('admins_page', pk=r_organization.id)
    else:
      messages.error(request, "The User isnt Registered to the system")

  context = {'page':page}

  return render(request,'base/add_delete_admin.html', context)


def delete_admin(request, pk):
  #gets user email, checks if already in the registered admins of organization, deletes user if already exists
  page = 'delete_admin'
  organization = RegisteredOrg.objects.get(id=pk)
  if request.method == 'POST':
    user_email = request.POST.get('email')
    try:
      user = User.objects.get(email=user_email)
    except:
      messages.error(request, "User Does Not Exist")
      return redirect('delete_admin', pk=organization.id)
    
    if user in organization.org_admins.all():
      organization.org_admins.remove(user)
      messages.success(request, f"{user_email} has been successfully removed from the organizations admins")
      return redirect('admins_page', pk=organization.id)

  context = {'page':page}
  return render(request, 'base/add_delete_admin.html', context)

def org_profile(request, pk):
  page = 'org_profile'
  org = RegisteredOrg.objects.get(id=pk)
  context = {'page':page, 'org':org}
  return render(request, 'base/profile.html', context)

def update_org_profile(request, pk):
  page = 'update_org_profile'
  org = RegisteredOrg.objects.get(id=pk)
  form = UpdateOrgForm(instance=org)

  if request.method == 'POST':
    org.org_name = request.POST.get('org_name')
    org.org_descr = request.POST.get('org_descr')
    org.org_avatar = request.FILES.get('org_avatar')
    org.save()
    return redirect('admins_page', pk=org.id)

  context = {'page':page, 'form':form}
  
  return render(request, 'base/update_form.html', context)



