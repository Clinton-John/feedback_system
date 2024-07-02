from django.contrib import admin
from django.urls import path
from . import views , views_admin

urlpatterns = [
    path('',views.home, name='home'),

# ------------ LOGIN, SIGNUP, LOGOUT ----- ###
path('signup/', views.signup_user, name='signup'),
path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name='logout'),

# ------------ REGISTER ORG ----- ###
path('register_org/', views.register_company, name='register_org'),
path('login_admin/', views.login_admin, name='login_admin'),

# the admins page should have an id field to specify which part should be accessed
path('admins_page/<str:pk>/', views.admins_page, name='admins_page'),

path('user_feedack/', views_admin.feedback_page, name="user_feedback")


]