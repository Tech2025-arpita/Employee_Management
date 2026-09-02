from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryUpdateView,
    CategoryDestroyView,
    # CategoryBulkImportView
)

urlpatterns = [
    path("category/",CategoryListCreateView.as_view(),name="category-list-create",),
    path("category/<int:pk>/",CategoryUpdateView.as_view(),name="category-update",),
    path("category/delete/<int:pk>/",CategoryDestroyView.as_view(),name="category-delete",),
    # path("categories/import/",CategoryBulkImportView.as_view(),name="category-bulk-import"),
]