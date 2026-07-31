from rest_framework import status
from rest_framework.test import APITestCase
from employee.models import Employees,PersonalDetails
from django.contrib.auth  import get_user_model
from department.models import Department
from country.models import Country
from datetime import date

class EmployeeViewTestCase(APITestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="testuser",password="testpassword")
        self.department=Department.objects.create(name="IT")
        self.country=Country.objects.create(name="India")
        self.employee=Employees.objects.create(name="Test Employee",email='test@gmail.com',
                                                    department=self.department,dob=date(1999,9,9),
                                                    salary='50000.00',
                                                    createdby=self.user,updatedby=self.user)
        self.personal_details = PersonalDetails.objects.create(employee=self.employee,address="Kolkata",
                                                               phone_number="9876543210",
                                                               zip_code="700001",country=self.country)
    def test_get_employee(self):
        # self.client.force_authenticate(user=self.user)
        response=self.client.get('/employee/emps/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_create_employee(self):
        # self.client.force_authenticate(user=self.user)
        data={
            "name":"Some Employee",
            "email":"some@gmail.com",
            "dob":date(2005,4,5),
            "salary":50000,
            "department":self.department.id,
            "personal_details": {
                "address": "Kolkata",
                "phone_number": "9999999999",
                "zip_code": "700001",
                "country": self.country.country_id
            },
            # "createdby":self.user.id,
            # "updatedby":self.user.id
        }
        response=self.client.post('/employee/emps/',data,format='json')

        # print(response.data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],'Some Employee')
        self.assertEqual(response.data['email'],'some@gmail.com')
        self.assertEqual(response.data['dob'],'2005-04-05')
        self.assertEqual(response.data['salary'],'50000.00')
        # self.assertEqual(response.data['createdby'],self.user.id)
        # self.assertEqual(response.data['updatedby'],self.user.id)

    def test_single_get_employee_id(self):
        # self.client.force_authenticate(user=self.user)
        response=self.client.get(f'/employee/emps/?emp_id={self.employee.id}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"],"Test Employee")

    def test_single_get_employee_by_name(self):
        response=self.client.get(f'/employee/emps/?emp_name=Test Employee')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Test Employee')
    
    def test_invalid_get_query_parameter(self):
        response=self.client.get(f'/employee/emps/?abc=123')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"],"Invalid Parameter")
    
    def test_get_by_employee_not_found(self):
        response=self.client.get(f'/employee/emps/?emp_id=999')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"],"No Employee found matching your search criteria.")

    def test_update_employee(self):
        self.client.force_authenticate(user=self.user)
        data={
            'name':'Updated Employee',
            'personal_details': {
                'address': 'New Delhi',
                'phone_number': '8888888888',
                'zip_code': '110001',
                'country': self.country.country_id
            }
        }
        response=self.client.put(f'/employee/emps/update/{self.employee.id}/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'Updated Employee')

    def test_delete_employee(self):
        self.client.force_authenticate(user=self.user)
        response=self.client.delete(f'/employee/emps/delete/{self.employee.id}/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employees.objects.filter(id=self.employee.id).exists())

#Filter
    def test_filter_employee_name_exact(self):
        response = self.client.get('/employee/emps/?name_exact=Test Employee')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_name_iexact(self):
        response = self.client.get('/employee/emps/?name_iexact=test employee')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_name_contains(self):
        response = self.client.get('/employee/emps/?name_contains=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_name_icontains(self):
        response = self.client.get('/employee/emps/?name_icontains=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_name_startswith(self):
        response = self.client.get('/employee/emps/?name_startswith=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_name_istartswith(self):
        response = self.client.get('/employee/emps/?name_istartswith=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_email_exact(self):
        response = self.client.get('/employee/emps/?email_exact=test@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_email_iexact(self):
        response = self.client.get('/employee/emps/?email_iexact=TEST@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_dob_exact(self):
        response = self.client.get('/employee/emps/?dob_exact=1999-09-09')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employee_dob_in(self):
        response = self.client.get('/employee/emps/?dob_in=1999-09-09,2005-04-05')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
