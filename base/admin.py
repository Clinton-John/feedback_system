from django.contrib import admin
from .models import User, RegisteredOrg, UserFeedback
# Register your models here.
# admin.site.register(User)

admin.site.register(RegisteredOrg)
admin.site.register(UserFeedback)



##using the Unfold to change the admin website