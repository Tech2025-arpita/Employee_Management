from django.urls import path
from .views import (
    InventoryListCreateView,
    InventoryUpdateView,
    InventoryDestroyView,
)

urlpatterns = [
    path("inventory/",InventoryListCreateView.as_view(),name="inventory-list-create",),
    path("inventory/<int:pk>/",InventoryUpdateView.as_view(),name="inventory-update",),
    path("inventory/delete/<int:pk>/",InventoryDestroyView.as_view(),name="inventory-delete",),
]