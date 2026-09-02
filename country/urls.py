from django.urls import path
from .views import CountryListCreate,CountryUpdateView,CountryDestroyView

urlpatterns=[
    path('countries/',CountryListCreate.as_view(),name='country_read_create'),
    path('countries/update/<int:pk>/', CountryUpdateView.as_view(), name='countries_update'),
    path('countries/delete/<int:pk>/', CountryDestroyView.as_view(), name='countries_delete'),
]