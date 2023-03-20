from django.db import models

# Create your models here.

class Payment(models.Model):
    payment_id= models.CharField(max_length=100)
    booking_id = models.CharField(max_length=100)
