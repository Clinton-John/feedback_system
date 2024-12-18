from django.conf import settings

from .models import RegisteredOrg, User, UserFeedback, FeedbackType, NotificationSettings
from django.contrib import messages
from .forms import OrgForm, UpdateOrgForm, OrgUpdateForm, AdminResponseForm
from django.shortcuts import render, redirect
from .models import UserFeedback, RegisteredOrg, OrgProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import qrcode
import os
from django.core.files import File
from django.core.files.base import ContentFile

from django.http import FileResponse
from django.core.mail import send_mail
from django.conf import settings
# from .signals import admin_added


def feedback_page(request, pk):
  # org = RegisteredOrg.objects.get(id=pk)
  org = RegisteredOrg.objects.get(id=pk)
  org_profile = OrgProfile.objects.get(id=pk)
  if request.method == 'POST':
    feedback_type_val = request.POST.get('feedback_type')

    feedback_type_inp, created = FeedbackType.objects.get_or_create(name=feedback_type_val)
    # feedback_type_inp = FeedbackType.objects.get(name=feedback_type_sval) #only if the feedback types are already typed in

    feedback = UserFeedback.objects.create(
      organization= org,
      user_email = request.POST.get('user_email'),
      feedback_type = feedback_type_inp,
      user_feedback = request.POST.get('user_feedback'),
      submited_to = org.org_email,
      user_ratings =request.POST.get('user_ratings')
    )
    return redirect('appreciation_page')

  context = {'org':org, 'org_profile':org_profile}


  return render(request, 'base/feedback_form.html', context)

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
      
      ### when the email functionaalities are added then it is also added
      # admin_added.send(sender=r_organization, user=user, organization=r_organization)


      return redirect('admins_page', pk=r_organization.id)
    else:
      messages.error(request, "The User isn't Registered to the system")

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
      try:
        organization.org_admins.remove(user)
        messages.success(request, f"{user_email} has been successfully removed from the organizations admins")
        return redirect('admins_page', pk=organization.id)
      except Exception as e:
        messages.error("Couldnt find the user in registered Administrators")
        return redirect('delete_admin', pk=organization.id)
      

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
  org_profile = OrgProfile.objects.get(id=pk)
  # form = UpdateOrgForm(instance=org)
  form = OrgUpdateForm(instance=org_profile)
  # form = OrgUpdateForm(instance=org_profile)

  if request.method == 'POST':
    # org.org_name = request.POST.get('org_name')
    #update the profile form
    org_profile.contact_email = request.POST.get('contact_email')
    org_profile.contact_phone = request.POST.get('contact_phone')
    org_profile.org_address = request.POST.get('org_address')
    org_profile.org_descr = request.POST.get('org_descr')
    org_profile.org_logo = request.FILES.get('org_logo')
    org_profile.org_website = request.POST.get('org_website')
    org_profile.org_facebook = request.POST.get('org_facebook')
    org_profile.org_twitter = request.POST.get('org_twitter')
    org_profile.org_instagram = request.POST.get('org_instagram')

    org_profile.save()

    #update the original created profile
    org.org_descr = request.POST.get('org_descr')
    org.org_avatar = request.FILES.get('org_avatar')
    org.save()
    return redirect('admins_page', pk=org.id)

  context = {'page':page, 'form':form, 'org':org}
  
  return render(request, 'base/update_form.html', context)

def org_settings(request, pk):
  org = RegisteredOrg.objects.get(id=pk)

  context = {'org':org}
  return render(request, 'base/settings.html', context)

def delete_org(request, pk):
  organization = RegisteredOrg.objects.get(id=pk)

  if request.user != organization.super_admin:
    messages.error("You cant Update the room !!!")

  if request.method == 'POST':
    organization.delete()
    return  redirect('home')
  
  context = {'obj':organization}
  return render(request, 'base/delete.html', context)
  

def individual_feedback(request, pk):
  individual_feedback = UserFeedback.objects.get(id=pk)
  org_feedback = individual_feedback.organization
  
  context = {'individual_feedback':individual_feedback, 'org_feedback':org_feedback}
  return render(request, 'base/feedback.html', context)

def delete_feedback(request, pk):
  feedback = UserFeedback.objects.get(id=pk)
  org_feedback = feedback.organization
  # all user admins page to be passed through the context dictionary.Converted to a list to allow iteration
  org_admins_db = list(org_feedback.org_admins.all())
  org_admins = list(org_feedback.org_admins.values_list('username', flat=True))
  # print(org_admins) 
  if request.method == 'POST':
    feedback.delete()
    return redirect('admins_page',org_feedback.id)

  context = {'obj':feedback, 'org_admins': org_admins, 'org_feedback':org_feedback}
  return render(request, 'base/delete.html', context)

# def reply_feedback(request, pk):
#   feedback = UserFeedback.objects.get(id=pk)

#   context = {'feedback':feedback}
#   return render(request, 'base/reply_email.html', context)

def reply_feedback(request, pk):
    feedback = UserFeedback.objects.get(id=pk)
    form = AdminResponseForm(instance=feedback)

    if request.method == 'POST':
        form = AdminResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            # Save the response to the database
            feedback = form.save(commit=False)
            feedback.response_sent = True  # Mark response as sent
            feedback.save()

            # Send email to the user with the response
            subject = "Response to Your Feedback"
            message = f"Dear User,\n\nThank you for your feedback!\n\nHere is our response:\n\n{feedback.admin_response}\n\nBest regards,\n{feedback.organization.org_name}"
            recipient_list = [feedback.user_email]
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
            
            messages.success(request, 'Response sent successfully!')
            return redirect('admins_page', id=feedback.organization.id)

    context = {'feedback': feedback, 'form': form}
    return render(request, 'base/reply_feedback.html', context)


## To specify that only the super admin can delete the feedback implemented by the line below 
  # if request.user not in org_admins:
  #   messages.error(request, "You cant Delete the Feedback !!!")
  # else:
  #     if request.method == 'POST':
  #       feedback.delete()
  #       return  redirect('admins_page', org_feedback.id)


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

  return ('org_settings', organization.id)

def get_org_code(request, pk):
  page = 'org_qrcode'
  org = RegisteredOrg.objects.get(id=pk)
  context = {'page':page, 'org':org}
  return render(request, 'base/site_basics.html', context)

def download_qrcode(request, pk):
  org = RegisteredOrg.objects.get(id=pk)
  organization_image = org.org_qr_code

  if organization_image:
    file_path = organization_image.path
    try:
      return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{org.org_name}_qrcode.png')
    except FileNotFoundError:
      messages.error("The Image doesnt exist")

    else:
      messages.error("The above organization doesnt have a QR code")

def notifications_settings(request, pk):
  page = 'notifications_settings'
  organization = RegisteredOrg.objects.get(id=pk)
  not_org = NotificationSettings.objects.get(organization=organization)
  # can be adjusted later
  notification_range = list(range(1,11))
  if request.method == "POST":
    not_org.notification_status = request.POST.get('notification_status')
    not_org.no_of_notifications = request.POST.get('num_of_notifications')

    not_org.save()


  #Now create the functionality to easily customize the user feedback page and pass the number of messages they want to the user page 
  context = {'page':page, 'organization':organization,'not_org':not_org, 'notification_range':notification_range }
  return render(request, 'base/site_basics.html', context)

