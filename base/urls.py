from django.contrib import admin
from django.urls import path
from . import views , views_admin

urlpatterns = [
    path('',views.home, name='home'),

# ------------ LOGIN, SIGNUP, LOGOUT ----- ###
path('signup/', views.signup_user, name='signup'),
path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name='logout'),

# ------------ LOGIN, SIGNUP, LOGOUT ----- ###
path('register_org/', views.register_company, name='register_org'),

]