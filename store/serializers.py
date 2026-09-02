from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    '''Store Serializer'''

    class Meta:
        model = Store
        fields = [
            "store_id",
            "store_name",
            "store_code",
            "store_add",
            "zip_code",
        ]
        read_only_fields = ["store_id", "store_code"]
