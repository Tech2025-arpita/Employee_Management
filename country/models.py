from django.conf import settings
from django.db import models

class Country(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,help_text="Country Name")
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="country_createdby_user")
    createddate = models.DateTimeField(null=True,blank=True,auto_now_add=True,help_text="Date Created")
    updatedby = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="country_updatedby_user")
    updateddate = models.DateTimeField(null=True,blank=True,auto_now=True,help_text="Last Updated Date")

    def __str__(self):
        return self.name