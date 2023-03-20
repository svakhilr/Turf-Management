
from rest_framework.views import  APIView
from accounts.serializers import UserSignupSerialiser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Accounts,VendorProfile
from .serializers import VendorProfileSerialiser
from .permissions import Isvendor
from turfs.models  import Booked_Timeslots
from turfs.serialiszers import BookedSerialiser



class VendorSignup(APIView):

    def post(self,request):
        serialiser = UserSignupSerialiser(data=request.data)
        if serialiser.is_valid():
            user = serialiser.save()
            user.role= 'VENDOR'
            user.save()
            return Response({"message":"Vendor Registration Successful"},status=status.HTTP_200_OK)
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)


class AddVendorDetails(APIView):
    permission_classes = [IsAuthenticated,Isvendor]
    
    def put(self,request):
        if request.user.role == 'VENDOR':
            vendor=VendorProfile.objects.get(user= request.user)
            serialiser = VendorProfileSerialiser(vendor,data=request.data)
            if serialiser.is_valid(raise_exception=True):
                serialiser.save()
                return Response(serialiser.data, status=status.HTTP_202_ACCEPTED)
            return Response(serialiser.errors)
        return Response({"message":"Not a vendor"},status=status.HTTP_401_UNAUTHORIZED)
    

class Booked_Slots(APIView):
    permission_classes=[IsAuthenticated, Isvendor]

    def get(self,request):
        vendor = VendorProfile.objects.get(user=request.user)
        bookings = Booked_Timeslots.objects.filter(turf__vendor=vendor)
        serialiser= BookedSerialiser(bookings, many=True)
        return Response(serialiser.data,status=status.HTTP_200_OK)
        
    

        
