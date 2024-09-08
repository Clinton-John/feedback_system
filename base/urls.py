from django.contrib import admin
from django.urls import path
from . import views , views_admin

urlpatterns = [
    path('',views.home, name='home'),

# ------------ LOGIN, SIGNUP, LOGOUT ----- ###
path('signup/', views.signup_user, name='signup'),
path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name='logout'),

# ------------- USER APRECIATION ----###
path('appreciation_page/', views.appreciation_page, name='appreciation_page'),


# ------------- USER PROFILE SECTION ----###
path('user_profile/<str:pk>', views.user_profile, name='user_profile'),
path('update_profile/<str:pk>', views.update_profile, name='update_profile'),

# ------------ REGISTER ORG ----- ###
path('register_org/', views.register_company, name='register_org'),

path('login_admin/', views.login_admin, name='login_admin'),


# ------------ ADMINS PAGE ----- ###
# the admins page should have an id field to specify which part should be accessed
path('admins_page/<str:pk>/', views.admins_page, name='admins_page'),
path('add_admin/<str:pk>/', views_admin.add_admin, name="add_admin"),#Delete Admin
path('update_org_profile/<str:pk>/', views_admin.update_org_profile, name="update_org_profile"),
path('org_profile/<str:pk>/', views_admin.org_profile, name="org_profile"),
path('delete_admin/<str:pk>/', views_admin.delete_admin, name="delete_admin"),

# ------------ FEEDBACK SECTION ----- ###
path('user_feedack/<str:pk>/', views_admin.feedback_page, name="user_feedback"),
path('individual_feedback/<str:pk>/', views_admin.individual_feedback, name="individual_feedback"),


# ------------ Organization settings section ----- ###
path('generate_code/<str:pk>/', views_admin.generate_qr_code, name="generate_qr_code"),
path('org_settings/<str:pk>', views_admin.org_settings, name='org_settings'),
path('get_org_code/<str:pk>', views_admin.get_org_code, name='get_org_code'),
path('download_qrcode/<str:pk>', views_admin.download_qrcode, name='download_qrcode'),

# ------------ Delete Section ----- ###
path('delete_org/<str:pk>', views_admin.delete_org, name='delete_org'),
path('delete_profile/<str:pk>', views.delete_profile, name='delete_profile'),
path('delete_feedback/<str:pk>', views_admin.delete_feedback, name='delete_feedback'),





]