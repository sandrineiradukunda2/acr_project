from django.contrib import admin
from Home.models import OTP, VerifyEmailLinkCounter, User
# Register your models here.
admin.site.register(User)
admin.site.register(VerifyEmailLinkCounter)
admin.site.register(OTP)
