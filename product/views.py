from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Product,ShipStationLabel
from .serializers import ProductSerializer
from inventory.models import Inventory
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# import os # NOSONAR
import requests

from django.conf import settings


logger = logging.getLogger(__name__)

request_data_key="Request Data : %s"

class ProductListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get("product_id")
        product_name = request.query_params.get("product_name")
        product_sku = request.query_params.get("product_sku")

        if product_id:
            queryset = self.get_queryset().filter(product_id=product_id)

        elif product_name:
            queryset = self.get_queryset().filter(product_name__iexact=product_name)

        elif product_sku:
            queryset = self.get_queryset().filter(product_sku__iexact=product_sku)

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message": "No Product Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # serializer = self.get_serializer(queryset, many=True) # NOSONAR
        # return Response(serializer.data)

        if product_name or product_sku or product_id:
            serializer = self.get_serializer(queryset.first())
        else:
            serializer = self.get_serializer(queryset,many=True)    
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.info(request_data_key, request.data)
        response = {}
        try:
            if Product.objects.filter(product_sku__exact=request.data.get("product_sku")
            ).exists():
                response["message"] = "Product SKU already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            #validate the data by the serializer
            serializer = ProductSerializer(data=request.data)

            if serializer.is_valid():
                product = serializer.save() #NOSONAR

                #create inventory automatically 
                # Inventory.objects.create(product=product,store=product.product_store)
                return Response(serializer.data,status=status.HTTP_201_CREATED)

            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong" # NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
class ProductUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
        logger.info(request_data_key, request.data)

        response = {}
        product_id = kwargs["pk"]

        try:
            product = Product.objects.filter(product_sku__iexact=request.data.get("product_sku"))

            if product.exclude(product_id=product_id).exists(): #another product using this sku check
                response["message"] = "Product SKU already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            kwargs["partial"] = True
            return self.update(request, *args, **kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class ProductDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        logger.info(request_data_key, request.data)
        response = {}
        product_id = kwargs["pk"]

        try:
            product = Product.objects.filter(product_id=product_id)
            if not product.exists(): #does the product exists that i want to delete
                response["message"] = "Product not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            product.delete() #return self.update(request, *args, **kwargs)  #NOSONAR

            response["message"] = "Product deleted successfully"
            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

# #CSV API
# class ProductBulkImportView(GenericAPIView):
#     parser_classes=[MultiPartParser]
#     def post(self, request, *args, **kwargs):
#         file_obj = request.FILES.get('file')
#         if not file_obj:
#             return Response({
#                 "error": "No file uploaded"
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         if not file_obj.name.endswith('.csv'):
#             return Response({
#                 "error": "Only CSV file formats are allowed"
#             }, status=status.HTTP_400_BAD_REQUEST)
#         # try:
#         #     csv_data = file_obj.read().decode('utf-8').splitlines()
#         #     reader = csv.DictReader(csv_data)
            
#         #     created_count = 0
#         #     errors = []

#         #     for index, row in enumerate(reader, start=1):
#         #         # --- THIK EIKHANE EI LINE-TA JOG KORUN ---
#         #         print(f"\n>>> TERMINAL-E DATA ASHCHE: {row}")
#         #         serializer = ProductSerializer(data=row)
#         try:
#             csv_data = file_obj.read().decode('utf-8').splitlines()
#             reader = csv.DictReader(csv_data)
            
#             created_count = 0
#             errors = []
#             for index, row in enumerate(reader, start=1):
#                 print(f"--- CSV Row {index} 's data: {row} ---")
#                 logger.info("Import Row %s: %s", index, row)
#                 serializer = ProductSerializer(data=row)
                
#                 if serializer.is_valid():
#                     sku = row.get('product_sku')
                    
#                     if not sku:
#                         errors.append({
#                             "row": index,
#                             "error": "product_sku is missing in this row"
#                         })
#                         continue
                        
#                     if not Product.objects.filter(product_sku__exact=sku).exists():
#                         serializer.save()
#                         created_count += 1

#                     else:
#                         errors.append({
#                             "row": index, "sku": sku,
#                             "error": "Product SKU already exists"
#                         })
#                 else:
#                     errors.append({
#                         "row": index,
#                         "errors": serializer.errors
#                     })

#             return Response({
#                 "message": f"Successfully imported {created_count} products.",
#                 "errors": errors
#             }, status=status.HTTP_201_CREATED)

#         except Exception as exp:
#             logger.exception(exp)
#             return Response({
#                 "message": "An error occurred during file parsing"
#             }, status=status.HTTP_400_BAD_REQUEST)


#Call third party Api(shipmentstation Api)

class ShipStationLabelView(GenericAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        labels = ShipStationLabel.objects.all() #bring all record from this table

        data = []

        for label in labels: #take all save record one by one 
            data.append({ #which field want to see that only keep
                "label_id": label.label_id,
                "shipment_id": label.shipment_id,
                "tracking_number": label.tracking_number,
                "carrier_id": label.carrier_id,
                "service_code": label.service_code,
                "status": label.status,
                "shipment_cost": label.shipment_cost,
                "label_format": label.label_format,
                "label_pdf_url": label.label_pdf_url,
                "tracking_url": label.tracking_url,
                "created_at": label.created_at,
            })

        return Response(data, status=status.HTTP_200_OK) #show into the reponse

    def post(self,request,*args,**kwargs):
        payload = {
            "shipment": {
                "carrier_id": "se-568902",
                "service_code": "ups_ground",

                "ship_to": {
                    "name": "John Doe",
                    "phone": "1234567890",
                    "address_line1": "123 Main Street",
                    "city_locality": "New York",
                    "state_province": "NY",
                    "postal_code": "10001",
                    "country_code": "US"
                },

                "ship_from": {
                    "name": "D&B Supply",
                    "phone": "2083421234",
                    "company_name": "D&B Supply",
                    "address_line1": "1000 W Overland Rd",
                    "city_locality": "Boise",
                    "state_province": "ID",
                    "postal_code": "83705",
                    "country_code": "US",
                    "address_residential_indicator": "no"
                },

                "packages": [
                    {
                        "package_code": "package",
                        "weight": {
                            "value": 10,
                            "unit": "ounce"
                        },
                        "dimensions": {
                            "unit": "inch",
                            "length": 10,
                            "width": 5,
                            "height": 4
                        }
                    }
                ]
            },

            "test_label": False,
            "label_download_type": "url",
            "label_format": "pdf"
        }

        headers = {
            "Content-Type": "application/json",
            "api-key": settings.SHIP_STATION_API_KEY
        }

        url = f"https://{settings.SHIP_STATION_V2_URL}/v2/labels"

        response = requests.post( #send post request to the shipmentstaion server
            url,
            headers=headers, #25
            json=payload
        )

        response_data = response.json() #which response send by shipstation keep it into this varr(come it into the django)

        if response.status_code in [200, 201]: #chk the data is correct or not 

            ShipStationLabel.objects.create(      #which data you want to show save into the db  
                label_id=response_data.get("label_id"),
                shipment_id=response_data.get("shipment_id"),
                tracking_number=response_data.get("tracking_number"),
                carrier_id=response_data.get("carrier_id"),
                service_code=response_data.get("service_code"),
                status=response_data.get("status"),
                shipment_cost=response_data.get("shipment_cost", {}).get("amount"), #supposse have no shipment cost then return empty dict without error
                label_format=response_data.get("label_format"),
                label_pdf_url=response_data.get("label_download", {}).get("pdf"), # get pdf url and save into the db
                tracking_url=response_data.get("tracking_url"),
                created_at=response_data.get("created_at"),
            )

        return Response(
            response_data,
            status=response.status_code #which response given by shipstation show it into the postman
        )

