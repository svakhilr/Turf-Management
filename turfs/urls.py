from django.urls import path
from . import views


urlpatterns=[
  path('addturf/',views.Addturf.as_view()),
  path('addimage/<int:id>/',views.AddTurfimage.as_view()),
  path('addtimeslot/<int:id>/',views.Addtimeslot.as_view()),
  path('viewslots/<int:id>/',views.ViewTimeslots.as_view()),
  path('bookslot/<int:id>/',views.Bookingslots.as_view()),
  
]