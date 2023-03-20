from rest_framework import serializers
from .models import Accounts




class UserSignupSerialiser(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only= True)
    role = serializers.CharField(read_only = True)

    class Meta:
        model = Accounts
        fields=['id','first_name','last_name','email','phone_number','password','password2','role']

    def validate(self,attrs):
        print("validate")
        if attrs['password']!= attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if len(attrs['phone_number'])< 10:
            raise serializers.ValidationError({"Phone number": "Invalid phone number"})

        return attrs
    
    def create(self, validated_data):
        print("create")
        user = Accounts.objects.create_user(validated_data['first_name'],validated_data['last_name'],validated_data['email'],validated_data['password'])
        print(user)
        user.phone_number= validated_data['phone_number']
        
        user.save()
        return user
    
class UserloginSerialiser(serializers.Serializer):
    email = serializers.EmailField()
    password =serializers.CharField()

