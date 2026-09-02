import csv
import time
import logging
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Product
from inventory.models import Inventory
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

logger=logging.getLogger(__name__)

class ProductExportView(GenericAPIView):
    '''Product Export'''

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        '''Export Product Data'''
        logger.info("Product Export Request")
        try:
            file_name="ProductExport"+str(time.time())+".csv" #file name 

            queryset=Product.objects.select_related(
                "product_brand",
                "product_category",
            ).all() #get related product from the db


            #FILTER OF PRODUCT_STATUS
            product_status = request.GET.get("product_status")

            #filter of enbale diasable
            if product_status:
                status_map = {
                    "Enable": "A",
                    "Disable": "I",
                }

                product_status = status_map.get(product_status)

                if product_status:
                    queryset = queryset.filter(product_status=product_status)

            #filter by Product_Name
            product_name=request.GET.get("product_name")

            if product_name:
                queryset = queryset.filter(product_name__iexact=product_name.strip())

            #filter by Product_sku
            product_sku = request.GET.get("product_sku")

            if product_sku:
                queryset = queryset.filter(
                    product_sku__iexact=product_sku.strip()
                )
            
            # print("SKU:", product_sku)
            # print("PRODUCTS:", list(queryset.values_list("product_sku", flat=True)))

            #filter by Brand_Code
            brand_code = request.GET.get("brand_code")

            if brand_code:
                queryset = queryset.filter(
                    product_brand__brand_code__iexact=brand_code.strip()
                )

            #filter by category_slug
            category_slug = request.GET.get("category_slug")

            if category_slug:
                queryset = queryset.filter(
                    product_category__slug__iexact=category_slug.strip()
                )

            #filter by store_name
            store_name = request.GET.get("store_name")
                        
            if store_name:
                queryset = queryset.filter(inventories__store__store_name__iexact=store_name.strip())

            if not queryset.exists():
                return Response({
                    "message":"No Product Data Found"
                },status=status.HTTP_404_NOT_FOUND)

            headers = {
                "product_name": "Product Name",
                "product_sku": "Product SKU",
                "short_desc": "Short Description",
                "long_desc": "Long Description",
                "product_status": "Product Status",
                "brand_code": "Brand Code",
                "category_slug": "Category Slug",
                "product_price": "Product Price",
                "store_name": "Store Name",
            }
            response=HttpResponse(content_type='text/csv')  #csv resposne is this type
            response["Content-Disposition"] = (
                f'attachment; filename="{file_name}"'
            ) #make the response downloadable
            writer=csv.writer(response) #csv writter
            writer.writerow(headers.values()) #write header row
            status_map = {
                "A": "Enable",
                "I": "Disable",
            }
            for product in queryset: #take product data
                inventories=Inventory.objects.filter(product=product).select_related("store") #take store data through the inventory
                store_names = [inventory.store.store_name for inventory in inventories] #12
                
                writer.writerow([
                    product.product_name,
                    # product.product_name,
                    product.product_sku,
                    product.short_desc,
                    product.long_desc,
                    status_map.get(product.product_status),
                    product.product_brand.brand_code,
                    product.product_category.slug,
                    product.product_price,
                    ", ".join(store_names),
                ])
            logger.info("Product Export Successfully Completed")

            return response  #return response of response=HttpResponse(content_type='text/csv') this
        
        except Exception as exp:
            logger.exception(
                "Product Export Exception : %s",
                exp
            )
            return Response(
                {
                    "message": "Something went wrong during export"
                },
                status=status.HTTP_400_BAD_REQUEST
            )