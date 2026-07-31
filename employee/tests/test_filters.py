from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

from employee.models import Employees,PersonalDetails
from department.models import Department
from country.models import Country

class TestEmployeeFilter(APITestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',password='testpassword')
        self.department=Department.objects.create(name="IT")
        self.country=Country.objects.create(name="India")
        self.employee= Employees.objects.create  ( name="Arpita Chatterjee",
                                                email='arpita@gmail.com',
                                                department=self.department,
                                                dob="1995-01-01",
                                                salary='50000.00',
                                                createdby=self.user,
                                                updatedby=self.user)
    def test_name_exact(self):
        response=self.client.get('/employee/emps/?name_exact=Arpita Chatterjee')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Arpita Chatterjee')

    def test_name_iexact(self):
        response=self.client.get(f'/employee/emps/?name_iexact=arpita chatterjee')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Arpita Chatterjee')

    def test_name_contains(self):
        response=self.client.get(f'/employee/emps/?name_contains=Arpita')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Arpita Chatterjee')

    def test_name_icontains(self):
        response=self.client.get(f'/employee/emps/?name_icontains=arpita')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Arpita Chatterjee')

    def test_name_startswith(self):
        response=self.client.get(f'/employee/emps/?name_startswith=Arpita')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Arpita Chatterjee')

    def test_name_istartswith(self):
        response=self.client.get(f'/employee/emps/?name_istartswith=arpita')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Arpita Chatterjee')

    #email
    def test_email_exact(self):
        response=self.client.get(f'/employee/emps/?email_exact=arpita@gmail.com')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['email'],'arpita@gmail.com')

    def test_email__iexact(self):
        response=self.client.get(f'/employee/emps/?email_iexact=ARPITA@GMAIL.COM')#This is i am sending 
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['email'],'arpita@gmail.com') #This is already have

    #dob
    def test_dob_exact(self):
        response=self.client.get(f'/employee/emps/?dob_exact=1995-01-01')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_dob_in(self):
        response=self.client.get('/employee/emps/?dob_in=1990-01-01,1995-01-01')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['dob'],'1995-01-01')
        
    def test_dob_range(self):
            response=self.client.get(f'/employee/emps/?dob_range=1990-01-01,2000-01-01')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_dob_gt(self):
            response=self.client.get(f'/employee/emps/?dob_gt=1990-01-01')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_dob_lt(self):
            response=self.client.get(f'/employee/emps/?dob_lt=2001-01-01')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_dob_gte(self):
            response=self.client.get(f'/employee/emps/?dob_gte=1990-01-01')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_dob_lte(self):
        response=self.client.get(f'/employee/emps/?dob_lte=2000-01-01')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['dob'],'1995-01-01')

    # def test_dob_date(self):
    #     response=self.client.get(f'/employee/emps/?dob_date=1995')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_dob_year(self):
        response=self.client.get(f'/employee/emps/?dob_year=1995')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['dob'],'1995-01-01')

    def test_salary_exact(self):
        response=self.client.get(f'/employee/emps/?salary_exact=50000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

    # def test_salary_exact(self):
    #     response=self.client.get(f'/employee/emps/?salary_exact=50000.00')
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data[0]['salary'],'50000.00')

    def test_salary_in(self):
        response=self.client.get(f'/employee/emps/?salary_in=40000.00,50000.00,80000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

    def test_salary_range(self):
        response=self.client.get(f'/employee/emps/?salary_range=20000.00,90000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

    def test_salary_gt(self):
        response=self.client.get(f'/employee/emps/?salary_gt=40000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

    def test_salary_lt(self):
        response=self.client.get(f'/employee/emps/?salary_lt=80000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

    def test_salary_gte(self):
        response=self.client.get(f'/employee/emps/?salary_gte=50000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

    def test_salary_lte(self):
        response=self.client.get(f'/employee/emps/?salary_lte=50000.00')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['salary'],'50000.00')

   
                
        