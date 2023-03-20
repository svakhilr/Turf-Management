from rest_framework import serializers
from accounts.models import VendorProfile
from accounts.serializers import UserSignupSerialiser

class VendorProfileSerialiser(serializers.ModelSerializer):
    user =UserSignupSerialiser(read_only=True)
    vendor_profile=serializers.ImageField(max_length=None, allow_empty_file=False)
    address1 = serializers.CharField()
    city = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    account_name = serializers.CharField()
    document=serializers.FileField(max_length=None, allow_empty_file=False)
    razorpay_id=serializers.CharField()
    ifsc_code=serializers.CharField()
    account_name=serializers.CharField()
    approved = serializers.BooleanField(read_only=True)
    class Meta:
        model= VendorProfile
        fields= ['id','vendor_profile','address1','city','pincode','account_number','ifsc_code','account_name','document','razorpay_id','approved','user']