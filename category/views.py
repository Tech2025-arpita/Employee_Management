from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# import csv #NOSONAR
# from rest_framework.parsers import MultiPartParser

logger = logging.getLogger(__name__)
request_data_key="Request Data : %s"

class CategoryListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get("category_id")
        name = request.query_params.get("name")
        parent_id=request.query_params.get("parent_id")

        allowed_params = [
            "category_id",
            "name",
            "parent_id"
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=400
                )

        if category_id:
            queryset = self.get_queryset().filter(category_id=category_id)

        elif name:
            queryset = self.get_queryset().filter(name__iexact=name)

        elif parent_id:
            queryset = self.get_queryset().filter(parent_id=parent_id)

        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {
                    "message": "No Category Found"  
                },
                status=404
            )

        # serializer = self.get_serializer(queryset, many=True) #NOSONAR
        # return Response(serializer.data)
        if category_id or name or parent_id:
            serializer=self.get_serializer(queryset.first())
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.info(request_data_key, request.data)
        response = {}
        try:
            if Category.objects.filter(slug__iexact=request.data.get("slug")).exists():
                response["message"] = "Slug already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            
            return self.create(request, *args, **kwargs)

        except Exception as exp:
            logger.exception(exp) 
            response["message"] = "Something went wrong" #NOSONAR
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class CategoryUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):
        logger.info(request_data_key, request.data)
        response = {}
        category_id = kwargs["pk"]
        try:
            category = Category.objects.filter(slug__iexact=request.data.get("slug"))
            if category.exclude(category_id=category_id).exists():
                response["message"] = "Slug already exists"
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            
            kwargs["partial"] = True
            return self.update(request, *args, **kwargs)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class CategoryDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def delete(self, request, *args, **kwargs):
        logger.info(request_data_key, request.data)
        response = {}
        category_id = kwargs["pk"]

        try:
            category = Category.objects.filter(category_id=category_id)
            if not category.exists():
                response["message"] = "Category not found"
                return Response(response,status=status.HTTP_404_NOT_FOUND)

            self.destroy(request, *args, **kwargs)

            response["message"] = "Category deleted successfully"
            return Response(response,status=status.HTTP_200_OK)

        except Exception as exp:
            logger.exception(exp)
            response["message"] = "Something went wrong"
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

 
# CSV API
# class CategoryBulkImportView(GenericAPIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, *args, **kwargs):
#         logger.info("Category Bulk Import Request")
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
#             imported_categories = []

#             for index, row in enumerate(reader, start=1):

#                 logger.info("Import Row %s: %s", index, row)

#                 data = {
#                     "name": row.get("name"),
#                     "description": row.get("description"),
#                     "parent_id": row.get("parent_id") or None
#                 }

#                 serializer = CategorySerializer(data=data) #NOSONAR

#                 if serializer.is_valid():

#                     name = row.get("name")
#                     parent_id = row.get("parent_id")

#                     if not name:
#                         errors.append({
#                             "row": index,
#                             "error": "Category name is missing"
#                         })
#                         continue

#                     if parent_id:
#                         if not Category.objects.filter(
#                             category_id=parent_id
#                         ).exists():
#                             errors.append({
#                                 "row": index,
#                                 "parent_id": parent_id,
#                                 "error": "Parent category not found"
#                             })
#                             continue

#                     category = serializer.save()
#                     created_count += 1

#                     imported_categories.append({
#                         "category_id": category.category_id,
#                         "name": category.name,
#                         "slug": category.slug,
#                         "description": category.description,
#                         "parent_id": category.parent_id_id
#                     })

#                 else:
#                     errors.append({
#                         "row": index,
#                         "errors": serializer.errors
#                     })

#             return Response(
#                 {
#                     "message": f"Successfully imported {created_count} categories.",
#                     "categories": imported_categories,
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