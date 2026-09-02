from django.urls import path
from .views import (
    StoreListCreateView,
    StoreUpdateView,
    StoreDestroyView,
    # StoreBulkImportView,
)

urlpatterns = [
    path("store/",StoreListCreateView.as_view(),name="store-list-create",),
    path("store/<int:pk>/",StoreUpdateView.as_view(),name="store-update",),
    path("store/delete/<int:pk>/",StoreDestroyView.as_view(),name="store-delete",),

    # path("store/import/", StoreBulkImportView.as_view()),
]