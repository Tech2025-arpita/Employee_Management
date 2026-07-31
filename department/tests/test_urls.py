from django.test import SimpleTestCase
from  django.urls import resolve,reverse
from department.views import(
    DepartmentListCreateView,
    DepartmentUpdateView,
    DepartmentDestroyView,
    )
class DeptUrlTest(SimpleTestCase):
    def test_department_get_create(self):
        url=reverse('department_read_create')
        self.assertEqual(resolve(url).func.view_class, DepartmentListCreateView)

    def test_update(self):
        url=reverse('department_update',kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DepartmentUpdateView)

    def test_delete(self):
        url=reverse('department_delete',kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DepartmentDestroyView) 