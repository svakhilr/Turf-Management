from django.db import models
from accounts.models import Accounts,VendorProfile


class Turf(models.Model):
    name = models.CharField(max_length=100,unique=True)
    type = models.CharField(max_length=200)
    max_player= models.IntegerField()
    description = models.TextField(max_length=250)
    location = models.CharField(max_length=100)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE,related_name='turfowner')
    vendor =models.ForeignKey(VendorProfile, on_delete=models.CASCADE,related_name='turfowner')

    def __str__(self):
        return self.name

class TurfImage(models.Model):
    turfimage = models.ImageField(upload_to='turfimages/')
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE,related_name='turf')

class Timeslots(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    price_per_hour = models.IntegerField()
    turf = models.ForeignKey(Turf,on_delete=models.CASCADE,related_name='turftime')

    def __str__(self):
        return f"{self.start_time} {self.end_time} {self.turf}"


class Booked_Timeslots(models.Model):
    timeslot = models.ForeignKey(Timeslots,on_delete=models.CASCADE,related_name='timeslots')
    booking_date = models.DateField()
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE,related_name='bookinguser')
    turf = models.ForeignKey(Turf,on_delete=models.CASCADE,related_name='turfbooking',null=True)

    def __str__(self):
        return f"{self.timeslot} {self.user}"


class Booking(models.Model):
    booking_status=(("Pending","Pending"),
                    ("Confirmed","Confirmed"),
                    ("Cancelled","Cancelled"),
                    ("NULL","Unassigned"))
    timeslot = models.ForeignKey(Timeslots, on_delete=models.CASCADE,related_name="bookedtimeslots")
    user     = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    date     = models.DateField()
    booked_date = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=20, choices=booking_status,default="NULL")
    booking_number = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"booked by {self.user}  'turf'  {self.timeslot.turf.name}"
