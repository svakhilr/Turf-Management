from django.urls import path
from . import views


urlpatterns=[
  path('userlist/',views.Userlist.as_view()),
  path('vendorlist/',views.VendorList.as_view()),
  path('vendor/<int:id>/',views.VendorDetails.as_view())
  
]