# from drf_yasg import openapi
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from .models import Store
from .serializers import StoreSerializer
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# import csv
# from rest_framework.parsers import MultiPartParser

logger=logging.getLogger(__name__)

# brn_prams = openapi.Schema(
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'brand_name': openapi.Schema(type=openapi.TYPE_STRING, description='Brand Name'),
#         'brand_desc': openapi.Schema(type=openapi.TYPE_STRING, description='Brand Description'),
#     }, required=['brand_name', 'brand_desc']
# )

class StoreListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Store.objects.all()
    serializer_class=StoreSerializer

    def get(self, request, *args, **kwargs):

        store_id = request.query_params.get("store_id")
        store_name = request.query_params.get("store_name")

        allowed_params = [
            "store_id",
            "store_name"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=400
                )

        if store_id:
            queryset = self.get_queryset().filter(
                store_id=store_id
            )

        elif store_name:
            queryset = self.get_queryset().filter(
                store_name__iexact=store_name
            )

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message":"No store found matching your search criteria."
                },
                status=404
            )

        # serializer = self.get_serializer(queryset, many=True)

        # return Response(serializer.data)

        if store_id or store_name:
            serializer = self.get_serializer(queryset.first())
        else:
            serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        '''Store create'''

        logger.info("Request Data : %s", request.data)
        response={}
        try:
            if Store.objects.filter(store_name__iexact=request.data.get("store_name")).exists():
                response["message"] = "Store already exists"
                return Response(response, status=400)
            return self.create(request, *args, **kwargs)
        
        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class StoreUpdateView(mixins.UpdateModelMixin,GenericAPIView):
    '''Storw update'''
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Store.objects.all()
    serializer_class=StoreSerializer

    def put(self,request,*args,**kwargs):
        '''Store update'''
        logger.info("Request Data : %s",request.data) #CLIENT SENDING DATA SAVE / SHOWING ON THE TERMINAL
        response={}
        store_id=kwargs['pk']
        try:
            store_objects = Store.objects.filter(store_name__iexact=request.data.get("store_name"))
            if store_objects.exclude(store_id=store_id).exists():
                response["message"] = "Store Name Already Exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            kwargs["partial"] = True 
            update_response=self.update(request, *args, **kwargs)
            return update_response

        # self.update(request,*args,**kwrags)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"

            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        
class StoreDestroyView(mixins.DestroyModelMixin,GenericAPIView):
    '''Store Delete'''

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Store.objects.all()
    serializer_class=StoreSerializer
    
    def delete(self,request,*args,**kwargs):
        logger.info("Request Data : %s",request.data)
        response={}
        store_id=kwargs['pk']
        try:
            store = Store.objects.filter(store_id=store_id)
            if not store.exists():
                response["message"]="Store not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request, *args, **kwargs)

            response["message"]="Store deleted successfully"
            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"]="Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        #CSV Api
# class StoreBulkImportView(GenericAPIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, *args, **kwargs):
#         logger.info("Store Bulk Import Request")

#         file_obj = request.FILES.get("file")

#         if not file_obj:
#             return Response(
#                 {
#                     "error": "No file uploaded"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if not file_obj.name.lower().endswith(".csv"):
#             return Response(
#                 {
#                     "error": "Only CSV file formats are allowed"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             csv_data = file_obj.read().decode("utf-8").splitlines()
#             reader = csv.DictReader(csv_data)

#             created_count = 0
#             errors = []
#             imported_stores = []

#             for index, row in enumerate(reader, start=1):
#                 serializer = StoreSerializer(data=row)

#                 if serializer.is_valid():

#                     store_name = row.get("store_name")
#                     store_code = row.get("store_code")

#                     if not store_name:
#                         errors.append({
#                             "row": index,
#                             "error": "store_name is missing in this row"
#                         })
#                         continue

#                     if not store_code:
#                         errors.append({
#                             "row": index,
#                             "error": "store_code is missing in this row"
#                         })
#                         continue

#                     if Store.objects.filter(
#                         store_name__iexact=store_name
#                     ).exists():
#                         errors.append({
#                             "row": index,
#                             "store_name": store_name,
#                             "error": "Store already exists"
#                         })
#                         continue

#                     if Store.objects.filter(
#                         store_code__iexact=store_code
#                     ).exists():
#                         errors.append({
#                             "row": index,
#                             "store_code": store_code,
#                             "error": "Store code already exists"
#                         })
#                         continue

#                     store = serializer.save()
#                     created_count += 1

#                     imported_stores.append({
#                         "store_id": store.store_id,
#                         "store_name": store.store_name,
#                         "store_code": store.store_code,
#                         "store_add": store.store_add,
#                         "zip_code": store.zip_code
#                     })

#                 else:
#                     errors.append({
#                         "row": index,
#                         "errors": serializer.errors
#                     })

#             return Response(
#                 {
#                     "message": f"Successfully imported {created_count} stores.",
#                     "stores": imported_stores,
#                     "errors": errors
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         except Exception as exp:
#             logger.exception(exp)

#             return Response(
#                 {
#                     "message": "An error occurred during file parsing"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )