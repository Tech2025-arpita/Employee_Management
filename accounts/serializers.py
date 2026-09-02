from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','email','password']
        extra_kwargs={
            "password":{
                "write_only":True
            }
        }
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This Email is already Registerd!")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

#Login serializer -->here all i have to chk the crednetial is exists in the db or not so this is completely diff from signup serializer

class LoginSerializer(serializers.Serializer): #login does not need directly connceted to the user so use this serializer insetad of Modelserializer
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        email=data.get('email')
        password=data.get('password')
        
        user=authenticate(
            username=email,   #is basically checking the login credentials against Django's User database.
            password=password
        )
        if user is None:
            raise serializers.ValidationError("Invalid Email or Password")
        
        refresh = RefreshToken.for_user(user) #for_user(user)-->Create JWT tokens for this particular authenticated user.

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token) #refrsh token retrieve/generate
        }






