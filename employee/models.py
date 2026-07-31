from django.conf import settings
from django.db import models
from department.models import Department
from country.models import Country


class Employees(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="department")
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="employee_createdby_user")
    createddate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatedby = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="employee_updatedby_user")
    updateddate = models.DateTimeField( auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.department} | {self.salary}"


class PersonalDetails(models.Model):
    employee = models.OneToOneField(Employees,on_delete=models.CASCADE,related_name="personal_details")
    address = models.TextField()
    phone_number = models.CharField( max_length=15)
    zip_code = models.CharField(max_length=10)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="employee_details")
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True, null=True,related_name="personal_details_createdby_user")
    createddate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatedby = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="personal_details_updatedby_user")
    updateddate = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.employee.name}'s details"

# class TestPersonalDetails(models.Model):
#     phone_number = models.CharField( max_length=25)

#     def __str__(self):
#         return f"{self.employee.name}'s details"