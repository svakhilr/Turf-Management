from django.urls import path
from . import views


urlpatterns=[
  path('paypal/create/order/', views.PayPalpayment.as_view(), name='ordercreate'),
  path('paypal/capture/order/',views.Checkout.as_view()),
  path('paypal/status/',views.PaymentResponse.as_view()),
]
  
