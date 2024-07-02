'''
views_admin
  --> generate qrcode /  generate new qrcode
  --> add company questions
  --> add administrators
  --> upgrade administrators
  --> remove administrators
  --> get stored qr code
'''

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