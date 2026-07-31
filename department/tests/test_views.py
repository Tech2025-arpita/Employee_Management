from rest_framework import status
# from rest_framework.response import Response
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from department.models import Department

class DepartViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',password='testpassword')
        self.department=Department.objects.create(name='IT',created_by=self.user,updated_by=self.user)

    def test_get_departments(self):
        response=self.client.get('/department/dept/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_create_departments(self):
        data={
            "name":"HR",
            "created_by":self.user.id,
            "updated_by":self.user.id,
        }
        response=self.client.post('/department/dept/',data,format='json')

        # print("\nSERIALIZER ERRORS:", response.data) 
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],'HR')


    def test_single_get_id(self):
        response=self.client.get(f'/department/dept/?deptid={self.department.id}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'IT')

    def test_single_get_by_name(self):
        response=self.client.get(f'/department/dept/?deptname=IT')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'IT')

    def test_invalid_get_query_parameter(self):
        response=self.client.get(f'/department/dept/?abc=123')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"],"Invalid Parameter")

    def test_get_by_dept_not_found(self):
        response=self.client.get(f'/department/dept/?deptid=999')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"],"No department found matching your search criteria.")

    def test_update_departments(self):
        data={
            "name":"Finance",
            "created_by":self.user.id,
            "updated_by":self.user.id,
        } 
        response=self.client.put(f'/department/dept/update/{self.department.id}/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertEqual(response.data['name'],'Finance')


    def test_delete_departments(self):
        response=self.client.delete(f'/department/dept/delete/{self.department.id}/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(id=self.department.id).exists())

