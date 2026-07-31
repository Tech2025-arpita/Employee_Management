from django.contrib.auth import get_user_model  
from django.test import TestCase
from country.models import Country

class CountryModelTestcase(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',password='testpassword')
        self.country=Country.objects.create(name="Test Country",createdby=self.user,updatedby=self.user)

    def test_country_creation(self):
        self.assertEqual(self.country.name,'Test Country')
        self.assertEqual(self.country.createdby,self.user)
        self.assertEqual(self.country.updatedby,self.user)
        self.assertIsNotNone(self.country.createddate)
        self.assertIsNotNone(self.country.updateddate)

    def test_model_string_representations(self):
        self.assertEqual(str(self.country), "Test Country")




