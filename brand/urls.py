from django.urls import path
from .views import (BrandListCreateView,BrandUpdateView,BrandDestroyView)

urlpatterns = [
    path("brands/", BrandListCreateView.as_view(), name="brand-list-create"),
    path("brands/<int:pk>/", BrandUpdateView.as_view(), name="brand-update"),
    path("brands/<int:pk>/delete/", BrandDestroyView.as_view(), name="brand-delete"),
    # path("brands/import/",BrandBulkImportView.as_view(),name="brand-bulk-import"),
]