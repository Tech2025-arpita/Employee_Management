from django.contrib.auth import get_user_model  
from django.test import TestCase
from department.models import Department

class DepartmentModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',password='testpassword')
        self.department = Department.objects.create(name='Test Department',created_by=self.user,updated_by=self.user)

    def test_department_creation(self):
        self.assertEqual(self.department.name,'Test Department')
        self.assertEqual(self.department.created_by, self.user)
        self.assertEqual(self.department.updated_by, self.user)
        self.assertIsNotNone(self.department.created_at)
        self.assertIsNotNone(self.department.updated_at)

    def test_model_string_representations(self):
        self.assertEqual(str(self.department), "Test Department") 
