from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Brand
# from rest_framework.validators import UniqueValidator

class BrandSerializer(serializers.ModelSerializer):
    '''Brand Serializer'''

    class Meta:
        model = Brand
        fields = [
            "brand_id",
            "brand_name",
            "brand_code",
            "brand_desc",
        ]
        read_only_fields = ["brand_id","brand_code"]