from django.contrib import admin
from .models import Accounts,VendorProfile,UserProfile
# Register your models here.


admin.site.register(Accounts)
admin.site.register(VendorProfile)
admin.site.register(UserProfile)
