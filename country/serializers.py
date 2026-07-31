from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import Country

class countrySerializer(serializers.ModelSerializer):
    name=serializers.CharField(
        max_length=100,validators=[UniqueValidator(queryset=Country.objects.all(),
                                                   message="This Name is Already Exists")])
    class Meta:
        model = Country
        fields = '__all__'
        extra_kwargs={
            "country_id":{
                "read_only":True
            },
            "createdby":{
                "read_only":True
            },
            "createddate":{
                "read_only":True
            },
            "updatedby":{
                "read_only":True
            },
            "updateddate":{
                "read_only":True
            }
        }

class CountrySmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = [
            "country_id",
            "name"
        ]     