from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import  UserSignupSerialiser
from accounts.models import Accounts,VendorProfile
from vendors.serializers import VendorProfileSerialiser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import Isadmin


class Userlist(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        
        if request.user.role == 'ADMIN':
            users = Accounts.objects.all()
            serialiser = UserSignupSerialiser(users, many=True)
            return Response(serialiser.data)
        return Response({"message":"not an authorised admin"},status=status.HTTP_401_UNAUTHORIZED)

class VendorList(APIView):
    permission_classes = [IsAuthenticated,Isadmin]
    def get(self,request):
        vendors = VendorProfile.objects.all()
        serialiser = VendorProfileSerialiser(vendors, many=True)
        return Response(serialiser.data)
    
class VendorDetails(APIView):
    permission_classes = [IsAuthenticated,Isadmin]

    def get(self,request,id):
        try:
            vendor = VendorProfile.objects.get(id=id)
            serialiser=VendorProfileSerialiser(vendor)
            return Response(serialiser.data)
        except:
            return Response({"message":"Not found"},status=status.HTTP_400_BAD_REQUEST)
        

    def post(self,request,id):
        try:
            vendor = VendorProfile.objects.get(id=id)
            if vendor.approved:
                return Response({"message":"Already approved"},status=status.HTTP_400_BAD_REQUEST)
            vendor.approved =True
            vendor.save()
            return Response({"message":"succesfully approved"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"message":"Not found"},status=status.HTTP_400_BAD_REQUEST)


