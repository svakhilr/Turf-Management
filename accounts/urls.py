from django.urls import path
from . import views


urlpatterns=[
  path('signup/',views.Usersignup.as_view(),name="user-signup"),
  path('signin/',views.UserLogin.as_view()),
  path('viewturfs/',views.Turfview.as_view()),
  path('nearbyturfs/',views.NearbyTurfs.as_view()),
  path('logout/', views.LogoutView.as_view(), name='auth_logout'),
  path('bookings/',views.ViewBookings.as_view())

]