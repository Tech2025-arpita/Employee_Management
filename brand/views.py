from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from .models import Brand
from .serializers import BrandSerializer
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# import csv #NOSONAR
# from rest_framework.parsers import MultiPartParser


logger=logging.getLogger(__name__)
request_data_key="Request Data : %s"

# brn_prams = openapi.Schema( #NOSONAR
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'brand_name': openapi.Schema(type=openapi.TYPE_STRING, description='Brand Name'),
#         'brand_desc': openapi.Schema(type=openapi.TYPE_STRING, description='Brand Description'),
#     }, required=['brand_name', 'brand_desc']
# )

class BrandListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer

    def get(self, request, *args, **kwargs):

        brand_id = request.query_params.get("brand_id")
        brand_name = request.query_params.get("brand_name")

        allowed_params = [
            "brand_id",
            "brand_name"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=400
                )

        if brand_id:
            queryset = self.get_queryset().filter(
                brand_id=brand_id
            )

        elif brand_name:
            queryset = self.get_queryset().filter(
                brand_name__iexact=brand_name
            )

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message":"No brand found matching your search criteria."
                },
                status=404
            )

        if brand_id or brand_name:
            serializer=self.get_serializer(queryset.first())
        else:
            serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        '''Brand create'''

        logger.info(request_data_key, request.data)
        response={}
        try:
            if Brand.objects.filter(brand_name__iexact=request.data.get("brand_name")).exists():
                response["message"] = "Brand already exists"
                return Response(response, status=400)
            return self.create(request, *args, **kwargs)
        
        except Exception as exp:
            logger.exception(exp)

class BrandUpdateView(mixins.UpdateModelMixin,GenericAPIView):
    '''Brand update'''
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer

    def put(self,request,*args,**kwargs):
        '''Brand update'''
        logger.info(request_data_key,request.data)
        response={}
        brand_id=kwargs['pk']
        try:
            brand_objects=Brand.objects.filter(brand_name__iexact=request.data.get("brand_name")) 
                                        #For better saftey so that there is no add but does not give use error 
            if brand_objects.exclude(brand_id=brand_id).exists():
                response["message"] = "Brand Name Already Exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

            kwargs["partial"] = True 
            update_response=self.update(request, *args, **kwargs)
            return update_response

        # self.update(request,*args,**kwrags)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"

            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        
class BrandDestroyView(mixins.DestroyModelMixin,GenericAPIView):
    '''Brand Delete'''
    queryset=Brand.objects.all()
    serializer_class=BrandSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def delete(self,request,*args,**kwargs):
        logger.info(request_data_key,request.data)
        response={}
        brand_id=kwargs['pk']
        try:
            brand = Brand.objects.filter(brand_id=brand_id)
            if not brand.exists():
                response["message"]="Brand not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request, *args, **kwargs)

            response["message"]="Brand deleted successfully"
            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"]="Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


# class BrandBulkImportView(GenericAPIView): #NOSONAR
#     parser_classes = [MultiPartParser]

#     def post(self, request, *args, **kwargs):
#         logger.info("Brand Bulk Import Request")
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
#             imported_brands = []

#             for index, row in enumerate(reader, start=1):
#                 logger.info("Import Row %s: %s", index, row)
#                 brand_name = row.get("brand_name")
#                 brand_desc = row.get("brand_desc")
#                 if not brand_name:
#                     errors.append({
#                         "row": index,
#                         "error": "brand_name is missing in this row"
#                     })
#                     continue

#                 #duplicate brand name chk
#                 if Brand.objects.filter(brand_name__iexact=brand_name).exists():
#                     errors.append({
#                         "row": index,
#                         "brand_name": brand_name,
#                         "error": "Brand already exists"
#                     })
#                     continue

#                 data = {
#                     "brand_name": brand_name,
#                     "brand_desc": brand_desc
#                 }

#                 serializer = BrandSerializer(data=data) #NOSONAR

#                 if serializer.is_valid():
#                     brand = serializer.save()
#                     created_count += 1
#                     imported_brands.append({
#                         "brand_id": brand.brand_id,
#                         "brand_name": brand.brand_name,
#                         "brand_code": brand.brand_code,
#                         "brand_desc": brand.brand_desc
#                     })

#                 else:
#                     errors.append({
#                         "row": index,
#                         "errors": serializer.errors
#                     })

#             return Response(
#                 {
#                     "message": f"Successfully imported {created_count} brands.",
#                     "brands": imported_brands,
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