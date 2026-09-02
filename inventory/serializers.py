from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()  #that is for which is not the part of direct models (to add extra field)
    # product_sku = serializers.SerializerMethodField()
    # brand_details = serializers.SerializerMethodField()
    store_details = serializers.SerializerMethodField()
    class Meta:
        model = Inventory
        fields = [
            "inv_id",
            "product",
            "product_details",
            # "product_sku",
            # "brand_details",
            "store",
            "store_details",
            "quantity",
        ]
        read_only_fields = ["inv_id"]

    # def get_product_name(self, obj):
    #     if obj.product:
    #         return obj.product.product_sku
    #     return None

    # def get_product_sku(self, obj):
    #     if obj.product:
    #         return obj.product.product_name
    #     return None
    
    # def get_product_name(self, obj):
    #     if obj.product:
    #         return obj.product.product_name
    #     return None

    # def get_product_sku(self, obj):
    #     if obj.product:
    #         return obj.product.product_sku
    #     return None
#This are for on the above which is writting that for only to add extra field to take related data 
    def get_product_details(self,obj):
        if obj.product:
            return{
                "product_id":obj.product.product_id,
                "product_name":obj.product.product_name,
                "product_sku":obj.product.product_sku
            }
        return None

    # def get_brand_details(self,obj):
    #     if obj.brand:
    #         return{
    #             "brand_id":obj.brand.brand_id,
    #             "brand_name":obj.brand.brand_name,
    #             "brand_code":obj.brand.brand_code,
    #             "brand_desc":obj.brand.brand_desc
    #         }
    
    def get_store_details(self, obj):
        if obj.store:
            return {
                "store_id": obj.store.store_id,
                "store_name": obj.store.store_name,
                "store_code": obj.store.store_code,
                "store_add": obj.store.store_add,
                "zip_code": obj.store.zip_code
            }
        return None