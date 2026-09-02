from django.urls import path
from .views import (
    ProductListCreateView,
    ProductUpdateView,
    ProductDestroyView,
    ShipStationLabelView,
)
from .product_import import (
    ProductBulkImportView,
    ProductBulkUpdateView,
)

from .product_export import(ProductExportView,)

urlpatterns = [
    path("product/",ProductListCreateView.as_view(),name="product-list-create",),
    path("product/<int:pk>/",ProductUpdateView.as_view(),name="product-update",),
    path("product/delete/<int:pk>/",ProductDestroyView.as_view(),name="product-delete",),
    #path of csv
    path("product/import/create/",ProductBulkImportView.as_view(),name="product-bulk-import"),
    path("product/import/update/",ProductBulkUpdateView.as_view(),name="product-bulk-update"),

    #export
    path("product/export/",ProductExportView.as_view(),name="product-export"),

    #api call url
    path("shipstation/label/",ShipStationLabelView.as_view(),name="shipstation-label"),
]