from django.urls import path
from . import views


urlpatterns=[
  path('vendorsignup/',views.VendorSignup.as_view()),
  path('addvendordetails/',views.AddVendorDetails.as_view()),
  path('viewbookings/',views.Booked_Slots.as_view())
  
]