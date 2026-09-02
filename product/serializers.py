from rest_framework import serializers
from .models import Product
from inventory.models import Inventory
from store.models import Store
from rest_framework.response import Response
from rest_framework import status
# from category.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):

    # store_ids = serializers.ListField(child=serializers.IntegerField(),write_only=True)
    store_ids = serializers.JSONField(write_only=True)
    store_ids_data=serializers.SerializerMethodField()
    product_store = serializers.SerializerMethodField()
    category_details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "product_id",
            "product_name",
            "product_sku",
            "short_desc",
            "long_desc",
            "product_status",
            "product_brand",
            "product_category",
            "category_details",
            "product_price",
            "store_ids",
            "store_ids_data",
            "product_store",
        ]

        
        read_only_fields = ["product_id", "category_details",]

    # def create(self, validated_data):
    #     store_ids = validated_data.pop("store_ids", []) # work with listing data

    #     product = Product.objects.create(**validated_data) #create product for one time

    #     for store_id in store_ids:
    #         Inventory.objects.create(
    #             product=product,
    #             store_id=store_id
    #         )

    #     return product

    def get_store_ids_data(self, obj):
        return list(
            Inventory.objects
            .filter(product=obj)
            .values_list("store_id", flat=True)
            .distinct()
        )

    # def validated_store_ids(self,value):
    #     if isinstance(value,int):
    #         value=[value]
    #     invalid_store_ids = [
    #         store_id
    #         for store_id in value
    #         if not Store.objects.filter(store_id=store_id).exists()
    # ]
        
    #     if invalid_store_ids:
    #         raise serializers.ValidationError(
    #             f"Store ID(s) {invalid_store_ids} do not exist."
    #         )

    #     return value

    # def create(self, validated_data):
    #     store_ids = validated_data.pop("store_ids", [])

    #     if isinstance(store_ids, int):
    #         store_ids = [store_ids]

    #     product = Product.objects.create(**validated_data)

    #     for store_id in store_ids:
    #         if not Store.objects.filter(store_id=store_id).exists():
    #             raise serializers.ValidationError(f"Store IDS {store_ids} Do Not Exists")
    #         Inventory.objects.create(
    #             product=product,
    #             store_id=store_id
    #         )

    #     return product

    def validate_store_ids(self, value):
        if isinstance(value, int):
            value = [value]

        for store_id in value:
            if not Store.objects.filter(store_id=store_id).exists():
                raise serializers.ValidationError(
                    f"Store ID {store_id} does not exist."
                )

        return value

    def create(self, validated_data):
        store_ids = validated_data.pop("store_ids", [])

        if isinstance(store_ids, int):
            store_ids = [store_ids]

        # for store_id in store_ids:
        #     if not Store.objects.filter(store_id=store_id).exists():
        #         return Response(
        #         {
        #             "message": f"Store ID {store_id} does not exist."
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        product = Product.objects.create(**validated_data)

        for store_id in store_ids:
            Inventory.objects.create(
                product=product,
                store_id=store_id
            )

        return product

    # def get_product_store(self, obj):
    #     inventories = Inventory.objects.filter(
    #         product__product_name=obj.product_name
    #     ).select_related("store")

    #     stores = {}

    #     for inventory in inventories:
    #         stores[inventory.store_id] = {
    #             "store_id": inventory.store_id,
    #             "store_name": inventory.store.store_name
    #         }

    #     return list(stores.values())

    # def get_product_store(self, obj):
    #     return list(
    #         Inventory.objects
    #         .filter(product__product_name=obj.product_name)
    #         .values_list("store_id", flat=True)
    #         .distinct() #store_id in list
    #     )

    def get_product_store(self, obj):
        inventories = Inventory.objects.filter(
            product__product_name=obj.product_name
        ).select_related("store") #select_related-->to get store name 
                                            #mapping this to the we have the id and the customer known it by name
        return list({
            inventory.store.store_name
            for inventory in inventories
        })

    #Product in which category
    def get_category_details(self, obj):
        category = obj.product_category  #find product Category full details

        return {
            "category_id": category.category_id,
            "name": category.name,
            "slug": category.slug,
            "parent": self.get_parent_category(category)
        }
    #Get full hirerchy
    def get_parent_category(self, category): # take one category
        if category.parent_id: #  this category has any parent or not 
            return {
                "category_id": category.parent_id.category_id,
                "name": category.parent_id.name,
                "slug": category.parent_id.slug,
                "parent": self.get_parent_category(category.parent_id)
            }

        return None


class ProductImportSerializer(serializers.Serializer):

    product_name = serializers.CharField()
    product_sku = serializers.CharField()
    short_desc = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    long_desc = serializers.CharField(required=False,allow_blank=True,allow_null=True)
    # product_status = serializers.CharField()
    # product_status = serializers.ChoiceField(choices=['A','I'])
    product_status = serializers.ChoiceField(choices=Product._meta.get_field("product_status").choices) #meta means access the db data(that created by djnago own)
    brand_code = serializers.CharField()
    # product_brand = serializers.IntegerField()
    category_slug = serializers.CharField()
    # product_category = serializers.CharField()
    # product_category = serializers.IntegerField()
    product_price = serializers.DecimalField(max_digits=10,decimal_places=2)
    store_name = serializers.CharField()
    # product_store = serializers.IntegerField()


