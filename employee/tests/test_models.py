from django.contrib.auth import get_user_model
from employee.models import Employees,PersonalDetails
from django.test import TestCase
from datetime import date
from department.models import Department
from country.models import Country

class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="testuser",password="testpassword")
        self.department=Department.objects.create(name="IT")
        self.employee=Employees.objects.create(name="Test Employee",email='test@gmail.com',
                                            department=self.department,dob=date(1999,9,9),
                                            salary='50000.00',
                                            createdby=self.user,updatedby=self.user)

    def test_employee_creation(self):
        self.assertEqual(self.employee.name,'Test Employee')
        self.assertEqual(self.employee.email,'test@gmail.com')
        self.assertEqual(self.employee.department,self.department)
        self.assertEqual(self.employee.dob,date(1999,9,9))
        self.assertEqual(self.employee.salary,"50000.00")
        self.assertEqual(self.employee.createdby,self.user)
        self.assertEqual(self.employee.updatedby,self.user)
        self.assertIsNotNone(self.employee.createddate)
        self.assertIsNotNone(self.employee.updateddate)

    def test_str_creation(self):
        expected_employee_string = f"{self.employee.id} | {self.employee.name} | {self.employee.department} | {self.employee.salary}"
        self.assertEqual(str(self.employee), expected_employee_string)
        
    # def __str__(self): 

    #     return f"{self.id} | {self.name} | {self.department} | {self.salary}" 

class PersonalDetailsModelTestCase(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="testuser",password="testpassword")
        self.department = Department.objects.create(name="IT")
        self.employee = Employees.objects.create(name="Test Employee",email="test@gmail.com",
                                                dob="1995-01-01",department=self.department,salary=50000)
        self.country = Country.objects.create(name="India")
        self.personal_details=PersonalDetails.objects.create(employee=self.employee,
                                                                   address='kolkata',
                                                                   phone_number='9874563210',
                                                                   zip_code='700001',
                                                                   country=self.country,
                                                                   createdby=self.user,
                                                                   updatedby=self.user
                                                                   )
    def test_personal_details_creation(self):
        self.assertEqual(self.personal_details.employee,self.employee)
        self.assertEqual(self.personal_details.address,'kolkata')
        self.assertEqual(self.personal_details.phone_number,'9874563210')
        self.assertEqual(self.personal_details.zip_code,'700001')
        self.assertEqual(self.personal_details.country,self.country)
        self.assertEqual(self.personal_details.createdby,self.user)
        self.assertEqual(self.personal_details.updatedby,self.user)
        self.assertIsNotNone(self.personal_details.createddate)
        self.assertIsNotNone(self.personal_details.updateddate)

    def test_model_string_representations(self):
        expected_details_string = f"{self.employee.name}'s details"
        self.assertEqual(str(self.personal_details), expected_details_string)

