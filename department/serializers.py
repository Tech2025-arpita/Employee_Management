from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department
from rest_framework.validators import UniqueValidator

class DeptSerializer(serializers.ModelSerializer):

    name=serializers.CharField(
        max_length=100,validators=[UniqueValidator(queryset=Department.objects.all(),
                                                   message="This Name is Already Exists")])
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs={
            "id":{
                "read_only":True
            },
            "created_by":{
                "read_only":True
            },
            "created_at":{
                "read_only":True
            },
            "updated_by":{
                "read_only":True
            },
            "updated_at":{
                "read_only":True
            }
        }

class DeptSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = [
            "id",
            "name"
        ]