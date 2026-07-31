'''
from django.urls import path
from .views import get_employess, create_employees, employee_detail
urlpatterns = [
    path("emps/",get_employess,name="employee-list"),
    path("emps/create/",create_employees,name="employee-create"),
    path("emps/<int:id>/",employee_detail,name="employee-detail"),
]
'''
from django.urls import path
from .views import (
    EmpListCreateView,
    EmployeeUpdateView,
    EmpDeleteView
    # PersonalDetailsListCreateView,
    # PersonalDetailsCompactView,
    )
urlpatterns=[
    path("emps/",EmpListCreateView.as_view(),name="emp_read_create"),
    path("emps/update/<int:pk>/",EmployeeUpdateView.as_view(),name="employee_update"),
    path("emps/delete/<int:pk>/",EmpDeleteView.as_view(),name="employee_delete"),

    # path("perosnal_details/",EmpListCreateView.as_view(),name="emp_read_create"),
    # path("emps/<int:pk>/",EmpDetailsView.as_view(),name="employee_detail")
]