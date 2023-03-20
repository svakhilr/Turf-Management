
from .serialiszers import TurfSerialiser,TurfimageSerialiser,TimeslotSerialiser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from  vendors.permissions import  Isvendor
from rest_framework import status
from .models import Turf,TurfImage,Timeslots,Booked_Timeslots,Booking

import random
import datetime

class Addturf(APIView):
    permission_classes= [IsAuthenticated,Isvendor]
    
    def post(self,request):
        serialiser = TurfSerialiser(data=request.data, context={'request': request})
        if serialiser.is_valid(raise_exception=True):
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)

        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)
    

class AddTurfimage(APIView):
    permission_classes= [IsAuthenticated,Isvendor]
    def post(self,request,id):
        try:
            print( Turf.objects.get(id=id))
            turf = Turf.objects.get(id=id)
            

        except:
            return Response({"message":"turf not found"},status=status.HTTP_400_BAD_REQUEST)
        
        image=request.FILES.get('turfimage', None)
        serialiser = TurfimageSerialiser(data={'turfimage':image})
        if serialiser.is_valid(raise_exception=True):
            images = request.FILES.getlist('turfimage')
            for image in images:
                TurfImage.objects.create(turfimage=image,turf=turf)
        return Response({"message":"success"},status=status.HTTP_201_CREATED)


class Addtimeslot(APIView):
    permission_classes= [IsAuthenticated,Isvendor]
    def post(self,request,id):
        try:
            turf = Turf.objects.get(id=id)

        except:
            return Response({"message":"Turf not found"})
        
        timeslots = request.data['timeslots']
        print(timeslots)
        for timeslot in timeslots:
            start_time = timeslot['start_time']
            end_time = timeslot['end_time']
            price_per_hour = timeslot['price_per_hour']
            Timeslots.objects.create(start_time=start_time,end_time=end_time,price_per_hour=price_per_hour,turf=turf)
        
        return Response({"message":"success"},status=status.HTTP_201_CREATED)
    
class ViewTimeslots(APIView):

    def get(self,request,id):
        print('hi')
        if Turf.objects.filter(id=id).exists():
            timeslots = Timeslots.objects.filter(turf__id=id)
            selected_date = str(request.query_params.get('selected_date', None))
            print(selected_date)
            date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
            print(date)
            serialiser = TimeslotSerialiser(timeslots, context={'date': date,'turf_id':id}, many= True )
            return Response(serialiser.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"Turf not found"},status=status.HTTP_400_BAD_REQUEST)
        

class Bookingslots(APIView):
    permission_classes= [IsAuthenticated]
    def post(self,request,id):
        print("hi")
        print(id)
        try:
            timeslot =Timeslots.objects.get(id=id)

        except:
            return Response({"message":"Invalid timeslot id"},status=status.HTTP_400_BAD_REQUEST)
        
        date = str(request.query_params.get('selected_date', None))
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        print(date)

        if Booked_Timeslots.objects.filter(timeslot = timeslot,booking_date=date).exists():
            return Response({"message":"Slot already booked"},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            booking = Booking.objects.create(timeslot=timeslot,user=request.user,date=date)
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            booking_no = str(random.randint(1111111111,9999999999))
            print(request.user.id)
            booking_number = current_date + str(request.user.id)+ booking_no
            booking.booking_number = booking_number
            booking.save()

            return Response({"message":"Booking intiated","Booking_id":booking_number},status=status.HTTP_201_CREATED)

