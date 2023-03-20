from django.contrib import admin
from .models import Turf,TurfImage,Timeslots,Booked_Timeslots,Booking

# Register your models here.
admin.site.register(Turf)
admin.site.register(TurfImage)
admin.site.register(Timeslots)
admin.site.register(Booked_Timeslots)
admin.site.register(Booking)
