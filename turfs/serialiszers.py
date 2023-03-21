from .models import Turf,TurfImage,Timeslots,Booked_Timeslots,Booking
from rest_framework import serializers
from geopy.geocoders import Nominatim
from accounts.models import VendorProfile


class TurfimageSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = TurfImage
        fields = ['turfimage']


class  TimeSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Timeslots
        fields=['id','start_time','end_time','price_per_hour','turf']


class TurfSerialiser(serializers.ModelSerializer):
    images =TurfimageSerialiser(source='turf',many= True,read_only=True)
    timeslots = TimeSerialiser(source='turftime',many=True, read_only=True)
    name = serializers.CharField()
    type =serializers.CharField()
    max_player = serializers.IntegerField()
    description = serializers.CharField()
    location = serializers.CharField()
    long = serializers.DecimalField(max_digits=8, decimal_places=3,required = False)
    lat = serializers.DecimalField(max_digits=8, decimal_places=3,required = False)

    class Meta:
        model = Turf
        fields= ['id','name','type','max_player','description','location','lat','long','images','timeslots']
    
    def validate_name(self, value):
        if Turf.objects.filter(name__iexact = value).exists():
            raise serializers.ValidationError("This name is already taken")
        return value
    
    def create(self, validated_data):
        user = self.context.get("request").user
        name = validated_data['name']
        type = validated_data['type']
        print(type)
        max_player = validated_data['max_player']
        description = validated_data['description']
        location = validated_data['location']
        vendor = VendorProfile.objects.get(user=user)
        print(max_player)
        geolocator = Nominatim(user_agent='turfs')
        location = geolocator.geocode(location)
        latitude, longitude = location.latitude, location.longitude
        turf = Turf.objects.create(name=name,type=type,max_player=max_player,description=description,location=location,lat=latitude,long=longitude,user=user,vendor=vendor)

        return turf


class TimeslotSerialiser(serializers.ModelSerializer):
    booked = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Timeslots
        fields = ['id','start_time','end_time','price_per_hour','turf','booked']
        
    def get_booked(self,obj):
        print('booking')
        turf_id= self.context.get('turf_id')
        date = self.context.get('date')
        
        if Booked_Timeslots.objects.filter(timeslot__id=obj.id,booking_date= date).exists():
            return True
        else:
            return False

class BookedSerialiser(serializers.ModelSerializer):
    timeslot = TimeSerialiser(read_only=True)
    class Meta:
        model = Booked_Timeslots
        fields=['timeslot','booking_date','user','turf']


class BookingslotSerialiser(serializers.ModelSerializer):

    class Meta:
        model =Booking
        fields='__all__'
