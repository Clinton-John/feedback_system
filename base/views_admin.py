
from .models import RegisteredOrg, User, UserFeedback, FeedbackType
from django.contrib import messages
from .forms import OrgForm, UpdateOrgForm

from django.shortcuts import render, redirect
from .models import UserFeedback, RegisteredOrg
from django.contrib.auth.decorators import login_required

from django.urls import reverse
import qrcode
import os
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile


def feedback_page(request, pk):
  org = RegisteredOrg.objects.get(id=pk)
  if request.method == 'POST':
    feedback_type_val = request.POST.get('feedback_type')

    feedback_type_inp, created = FeedbackType.objects.get_or_create(name=feedback_type_val)
    # feedback_type_inp = FeedbackType.objects.get(name=feedback_type_sval) #only if the feedback types are already typed in


    feedback = UserFeedback.objects.create(
      organization= org,
      user_email = request.POST.get('user_email'),
      feedback_type = feedback_type_inp,
      user_feedback = request.POST.get('user_feedback'),
      user_ratings =request.POST.get('user_ratings')
    )
    return redirect('appreciation_page')

  context = {'org':org}


  return render(request, 'base/qrcode_form.html', context)

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

def org_settings(request, pk):
  org = RegisteredOrg.objects.get(id=pk)

  context = {'org':org}
  return render(request, 'base/settings.html', context)


def individual_feedback(request, pk):
  individual_feedback = UserFeedback.objects.get(id=pk)
  context = {'individual_feedback':individual_feedback}
  return render(request, 'base/feedback.html', context)

def generate_qr_code(request, pk):
  organization = RegisteredOrg.objects.get(id=pk)
  org_url = request.build_absolute_uri(reverse('user_feedback', args=[pk]))

  qr = qrcode.QRCode(
    version = 1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )
  qr.add_data(org_url)
  qr.make(fit=True)

  org_qr_img = qr.make_image(fill='black', back_color='white')
  img_filename = f'{organization.org_name}_qr.png'
  img_path = os.path.join(settings.MEDIA_ROOT, img_filename)
  org_qr_img.save(img_path, 'PNG')

  with open(img_path, 'wb') as img_file:
    org_qr_img.save(img_file, 'PNG')

    # organization.org_qr_code.save(img_filename,File(img_file), save=True)
    # Save the image path to the database
  organization.org_qr_code.save(img_filename, ContentFile(open(img_path, 'rb').read()), save=True)


  if os.path.exists(img_path):
    os.remove(img_path)

  messages.success(request,'QR code successfully generated')

  return redirect('org_settings', organization.id)

def get_org_code(request, pk):
  page = 'org_qrcode'
  org = RegisteredOrg.objects.get(id=pk)
  context = {'page':page, 'org':org}
  return render(request, 'base/site_basics.html', context)