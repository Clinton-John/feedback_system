from django.contrib import admin
from .models import User, RegisteredOrg, UserFeedback, FeedbackType, Profile, OrgProfile,FormSubmissionCounter, NotificationSettings
# Register your models here.
# admin.site.register(User)

admin.site.register(RegisteredOrg)
admin.site.register(Profile)
admin.site.register(OrgProfile)
admin.site.register(UserFeedback)
admin.site.register(FeedbackType)
admin.site.register(FormSubmissionCounter)
admin.site.register(NotificationSettings)



##using the Unfold to change the admin website