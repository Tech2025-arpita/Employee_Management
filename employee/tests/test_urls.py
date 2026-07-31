from django.test import SimpleTestCase
from django.urls import resolve,reverse
from employee.views import (
    EmpListCreateView,
    EmployeeUpdateView,
    EmpDeleteView,
)
class EmployeeUrlTest(SimpleTestCase):
    def test_get_create_url(self):
        url=reverse('emp_read_create')
        self.assertEqual(resolve(url).func.view_class,EmpListCreateView)

    def test_update_url(self):
        url=reverse('employee_update',kwargs={"pk":1})
        self.assertEqual(resolve(url).func.view_class,EmployeeUpdateView)

    def test_delete_url(self):
        url=reverse('employee_delete',kwargs={"pk":1})
        self.assertEqual(resolve(url).func.view_class,EmpDeleteView)