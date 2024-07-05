'''
views_admin
  --> generate qrcode /  generate new qrcode
  --> add company questions
  --> add administrators
  --> upgrade administrators
  --> remove administrators
  --> get stored qr code
'''

from .models import RegisteredOrg, User, UserFeedback
from django.contrib import messages

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

  return render(request,'base/add_admin_form.html')


