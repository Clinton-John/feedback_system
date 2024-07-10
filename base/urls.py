from django.contrib import admin
from django.urls import path
from . import views , views_admin

urlpatterns = [
    path('',views.home, name='home'),

# ------------ LOGIN, SIGNUP, LOGOUT ----- ###
path('signup/', views.signup_user, name='signup'),
path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name='logout'),

# ------------- USER PROFILE SECTION ----###
path('user_profile/<str:pk>', views.user_profile, name='user_profile'),
path('update_profile/<str:pk>', views.update_profile, name='update_profile'),

# ------------ REGISTER ORG ----- ###
path('register_org/', views.register_company, name='register_org'),
path('login_admin/', views.login_admin, name='login_admin'),


# ------------ ADMINS PAGE ----- ###

# the admins page should have an id field to specify which part should be accessed
path('admins_page/<str:pk>/', views.admins_page, name='admins_page'),
path('user_feedack/', views_admin.feedback_page, name="user_feedback"),
path('add_admin/<str:pk>/', views_admin.add_admin, name="add_admin"),#Delete Admin
path('update_org_profile/<str:pk>/', views_admin.update_org_profile, name="update_org_profile"),
path('org_profile/<str:pk>/', views_admin.org_profile, name="org_profile"),
path('delete_admin/<str:pk>/', views_admin.delete_admin, name="delete_admin")



]