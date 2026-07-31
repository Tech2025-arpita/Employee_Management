from django.urls import path
from .views import DepartmentListCreateView,DepartmentUpdateView,DepartmentDestroyView

urlpatterns=[
    path('dept/',DepartmentListCreateView.as_view(),name='department_read_create'),
    path('dept/update/<int:pk>/',DepartmentUpdateView.as_view(), name='department_update'),
    path('dept/delete/<int:pk>/',DepartmentDestroyView.as_view(),name='department_delete')
]