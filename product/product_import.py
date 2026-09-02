import logging
import pandas as pd

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, ProductImportSerializer

from brand.models import Brand
from category.models import Category
from store.models import Store
from inventory.models import Inventory

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)

class ProductBulkImportView(GenericAPIView):
    """Product Bulk Import"""

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = ProductImportSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        """Product Bulk Create"""

        logger.info("Product Bulk Import Request")

        files = request.FILES.get("file")

        if not files:
            return Response(
                {
                    "message": "No files found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file_extension = str(files.name.split(".")[-1]).lower()

        if file_extension not in ["csv", "xlsx"]:
            return Response(
                {
                    "message": "Invalid file type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Read CSV 
            if file_extension == "csv":
                read_df = pd.read_csv(files).to_dict("records")
            else:
                read_df = pd.read_excel(files).to_dict("records")

            created_products = []
            errors = []

            for index, row in enumerate(read_df, start=2):

                logger.info("Import Row %s : %s",index,row)
                import_serializer = ProductImportSerializer(data=row)

                if not import_serializer.is_valid():

                    errors.append({
                        "row": index,
                        "errors": import_serializer.errors
                    })

                    continue

                data = import_serializer.validated_data #Keep clean and validated data into this varr

                product_sku = data["product_sku"]

                if Product.objects.filter(product_sku__iexact=product_sku).exists():

                    errors.append({
                        "row": index,
                        "product_sku": product_sku,
                        "error": "Product SKU already exists"
                    })

                    continue


                brand = Brand.objects.filter(brand_code__iexact=data["brand_code"]).first() #objection

                if not brand:

                    errors.append({
                        "row": index,
                        "brand_code": data["brand_code"],
                        "error": "Brand not found"
                    })

                    continue

                # brand = Brand.objects.filter(
                #     brand_code__iexact=data["brand_code"]
                # ).first()
                                        #if i want to create brand_code forcefully
                # if not brand:
                #     brand = Brand.objects.create(
                #         brand_code=data["brand_code"],
                #         brand_name=data["brand_code"]
                #     )


                category = Category.objects.filter(slug__iexact=data["category_slug"]).first()

                if not category:

                    errors.append({
                        "row": index,
                        "category_slug": data["category_slug"],
                        "error": "Category not found"
                    })

                    continue


                store = Store.objects.filter(store_name__iexact=data["store_name"]).first() #take the data from the user site

                if not store:

                    errors.append({
                        "row": index,
                        "store_name": data["store_name"],
                        "error": "Store not found"
                    })

                    continue

                #payload
                product_data = {
                    "product_name": data["product_name"],
                    "product_sku": data["product_sku"],
                    "short_desc": data.get("short_desc"),
                    "long_desc": data.get("long_desc"),
                    "product_status": data["product_status"],  #AS THE FIELD OF THE DB AND THE CSV ARE NOT SAME 
                    "product_brand": brand.brand_id,
                    "product_category": category.category_id,
                    "product_price": data["product_price"],
                    "store_ids": [store.store_id]
                }


                product_serializer = ProductSerializer(data=product_data)  #before creating product we can serialize and validate data

                if product_serializer.is_valid():
                    product = product_serializer.save()
                    # Inventory.objects.create(product=product,store=product.product_store)
                    created_products.append({
                        "product_id": product.product_id,
                        "product_name": product .product_name,
                        "product_sku": product.product_sku,                                                                                                
                        "brand_code": product.product_brand.brand_code,
                        "category_slug": product.product_category.slug,
                        "product_price": str(
                            product.product_price
                        ),
                        "store_name": store.store_name 
                    })

                else:

                    errors.append({
                        "row": index,
                        "errors": product_serializer.errors
                    })

            logger.info("Created Products : %s",len(created_products))

            return Response(
                {
                    "message": (
                        f"Successfully imported "
                        f"{len(created_products)} products."
                    ),
                    "products": created_products,
                    "errors": errors
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as exp:

            logger.exception(exp)

            return Response(
                {
                    "message": "Something is occuriing during parsing"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ProductBulkUpdateView(GenericAPIView):
    """Product bulk update"""
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = ProductImportSerializer
    parser_classes = [MultiPartParser]

    def put(self, request, *args, **kwargs):
        """Product bulk update"""

        logger.info("Product Bulk Update Request")

        files = request.FILES.get("file", None)

        if not files:
            return Response(
                {
                    "message": "No files found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file_extension = str(files.name.split(".")[-1]).lower()
        if file_extension not in ["csv", "xlsx"]:
            return Response(
                {
                    "message": "Invalid file type"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Read CSV 
            if file_extension == "csv":
                read_df = pd.read_csv(files).to_dict("records")
            else:
                read_df = pd.read_excel(files).to_dict("records")

            updated_products = []
            errors = []

            for index, row in enumerate(read_df, start=2):

                logger.info(
                    "Update Row %s : %s",
                    index,
                    row
                )


                product_sku = row.get("product_sku")

                if (product_sku is None or pd.isna(product_sku) or not str(product_sku).strip()):
                    errors.append({
                        "row": index,  #if one of the condition(in if) is true then the error will be save 
                        "error": "product_sku is required"
                    })
                    continue

                product_sku = str(product_sku).strip() #Doing clean and keep it into the varriable

                product = Product.objects.filter(product_sku__iexact=product_sku).first() #by sku seraching exact product

                if not product:
                    errors.append({
                        "row": index,
                        "product_sku": product_sku,
                        "error": "Product not found"
                    })
                    continue


                data = {}

                fields = [
                    "product_name",
                    "short_desc",
                    "long_desc",
                    "product_status",
                    "product_price"
                ]

                for field in fields:
                    if field in row and not pd.isna(row.get(field)):
                        data[field] = row[field]
        
                if ("brand_code" in row and not pd.isna(row.get("brand_code"))):
                    brand = Brand.objects.filter(
                        brand_code__iexact=str(
                            row["brand_code"]
                        ).strip()
                    ).first()

                    if not brand:
                        errors.append({ 
                            "row": index,
                            "brand_code": row["brand_code"],
                            "error": "Brand not found"
                        })
                        continue

                    data["product_brand"] = brand.brand_id


                if ("category_slug" in row and not pd.isna(row.get("category_slug"))):

                    category = Category.objects.filter(slug__iexact=str(row["category_slug"]).strip()).first()
                    if not category:
                        errors.append({
                            "row": index,
                            "category_slug": row["category_slug"],
                            "error": "Category not found"
                        })
                        continue

                    data["product_category"] = category.category_id

                if ("store_name" in row and not pd.isna(row.get("store_name"))):

                    store = Store.objects.filter(
                        store_name__iexact=str(
                            row["store_name"]
                        ).strip()
                    ).first()

                    if not store:
                        errors.append({
                            "row": index,
                            "store_name": row["store_name"],
                            "error": "Store not found"
                        })
                        continue

                    data["product_store"] = store.store_id

                if not data:
                    errors.append({
                        "row": index,
                        "product_sku": product_sku,
                        "error": "No fields provided for update"
                    })
                    continue


                product_serializer = ProductSerializer(product,data=data,partial=True)

                if product_serializer.is_valid():
                    product = product_serializer.save()
                    updated_products.append({
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "product_sku": product.product_sku,
                        "brand_code": (
                            product.product_brand.brand_code
                        ),
                        "category_slug": (
                            product.product_category.slug
                        ),
                        "product_price": str(
                            product.product_price
                        ),
                        "store_name": (
                            product.product_store.store_name
                        )
                    })

                else:
                    errors.append({
                        "row": index,
                        "errors": product_serializer.errors
                    })

            logger.info("Updated Products: %s",len(updated_products))

            return Response(
                {
                    "message": (
                        f"Successfully updated "
                        f"{len(updated_products)} products."
                    ),
                    "products": updated_products,
                    "errors": errors
                },
                status=status.HTTP_200_OK
            )

        except Exception as exp:
            logger.exception(exp)
            return Response(
                {
                    "message": "An error occurred during file parsing"
                },
                status=status.HTTP_400_BAD_REQUEST
            )