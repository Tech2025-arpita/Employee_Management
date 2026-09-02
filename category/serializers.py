from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category
# from rest_framework.validators import UniqueValidator

class CategorySerializer(serializers.ModelSerializer):

    parent_category_details = serializers.SerializerMethodField()
    # slug = serializers.SlugField(required=False,validators=[UniqueValidator(
    #     queryset=Category.objects.all(),message="Slug already exists")])

    class Meta:
        model = Category
        fields = [
            "category_id",
            "name",
            "slug",
            "description",
            "parent_category_details",
            "parent_id",
        ]
        read_only_fields = ["category_id", "slug"]

    def get_parent_category_details(self, obj):
        if obj.parent_id:
            return {
                "category_id": obj.parent_id.category_id,
                "name": obj.parent_id.name,
                "slug": obj.parent_id.slug,
                "parent": self.get_parent_category_details(obj.parent_id)
            }

        return None
