from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class InventoryListCreateView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request, *args, **kwargs):

        inv_id = request.query_params.get("inv_id")
        product_sku = request.query_params.get("product_sku")
        store_id = request.query_params.get("store_id")

        allowed_params = [
            "inv_id",
            "product_sku",
            "store_id",
        ]

        for param in request.query_params:
            if param not in allowed_params:
                return Response(
                    {
                        "message": "Invalid Parameter"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        queryset = self.get_queryset()

        if inv_id:
            queryset = queryset.filter(inv_id=inv_id)

        elif product_sku:
            queryset = queryset.filter(
                product__product_sku__iexact=product_sku
            )

        elif store_id:
            queryset = queryset.filter(
                store__store_id=store_id
            )

        if not queryset.exists():
            return Response(
                {
                    "message": "No Inventory Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # serializer = self.get_serializer(queryset, many=True)

        # return Response(serializer.data)

        if inv_id or product_sku or store_id:
            serializer = self.get_serializer(queryset.first()) #For single data in postman in json not in list
        else:
            serializer = self.get_serializer(queryset,many=True)    
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        logger.info("Request Data : %s", request.data)
        response = {}

        try:

            if Inventory.objects.filter(
                product=request.data["product"],  #here it is creating product against multiple store
                store=request.data["store"]
            ).exists():

                response["message"] = "Inventory already exists for this store"

                return Response(
                    response,
                    status=status.HTTP_400_BAD_REQUEST
                )

            return self.create(request, *args, **kwargs)

        except Exception as exp:

            logger.exception(exp)

            response["message"] = "Something went wrong"

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )
class InventoryUpdateView(
    mixins.UpdateModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response(
            {
                "message": f"update is only allowed for just giving single id"
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


    def put(self, request, *args, **kwargs):

        logger.info("Request Data : %s", request.data)

        response = {}

        try:
            kwargs["partial"] = True

            return self.update(request, *args, **kwargs)

        except Exception as exp:

            logger.exception(exp)

            response["message"] = "Something went wrong"

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        #     kwargs["partial"] = True

        #     return self.update(request, *args, **kwargs)

        # except Exception as exp:

        #     logger.exception(exp)

        #     response["message"] = "Something went wrong"

        #     return Response(
        #         response,
        #         status=status.HTTP_400_BAD_REQUEST
            # )
class InventoryDestroyView(
    mixins.DestroyModelMixin,
    GenericAPIView
):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def delete(self, request, *args, **kwargs):

        logger.info("Request Data : %s", request.data)

        response = {}

        inv_id = kwargs["pk"]

        try:

            inventory = Inventory.objects.filter(inv_id=inv_id)

            if not inventory.exists():

                response["message"] = "Inventory not found"

                return Response(
                    response,
                    status=status.HTTP_404_NOT_FOUND
                )

            self.destroy(request, *args, **kwargs)

            response["message"] = "Inventory deleted successfully"

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except Exception as exp:

            logger.exception(exp)

            response["message"] = "Something went wrong"

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )