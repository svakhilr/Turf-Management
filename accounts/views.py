
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerialiser,UserloginSerialiser
from django.contrib.auth import  authenticate
from turfs.serialiszers import TurfSerialiser
from turfs.models import Turf
from geopy.distance import distance
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Usersignup(APIView):
    def post(self,request):
        serialiser = UserSignupSerialiser(data=request.data)
        if serialiser.is_valid(raise_exception=True):
            print("hi")
            print(serialiser.validated_data)
            user=serialiser.save()
            user.role = 'CUSTOMER'
            user.save()
            return Response({"message":"Successfully registered"},status=status.HTTP_202_ACCEPTED)
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):
    def post(self,request):
        serialiser = UserloginSerialiser(data = request.data)
        if serialiser.is_valid():
            email = serialiser.validated_data['email']
            password = serialiser.validated_data['password']
            user = authenticate(email = email,password = password)

            if user:
                token = get_tokens_for_user(user)
                print(token)
                return Response({"message":"Successfully LogedIn","tokens":token},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Provide proper details"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)  
        

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print("hi")
        try:
            
            refresh_token = request.data["refresh_token"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Turfview(APIView):

    def get(self,request):  
        turf = Turf.objects.all()
        serialiser = TurfSerialiser(turf, many= True)
        return Response(serialiser.data , status=status.HTTP_202_ACCEPTED)
    

class NearbyTurfs(APIView):

    def get(self,request):
        
        if  'latitude' not in request.data:
            return Response({"message":"provide latitude"},status=status.HTTP_400_BAD_REQUEST)
        
        latitude = request.data["latitude"]
        
        longitude = request.data['longitude']
        print(latitude) 
        user_location = (float(latitude), float(longitude))
        nearby_turfs = []
        for turf in Turf.objects.all():
            turf_location = (turf.lat, turf.long)
            turf_distance = distance(user_location, turf_location).km
            if turf_distance <= 10:
                nearby_turfs.append(turf)
        serialized_places = TurfSerialiser(nearby_turfs, many=True).data
        return Response(serialized_places,status=status.HTTP_200_OK)
    




