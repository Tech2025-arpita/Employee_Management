from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from country.models import Country

class CountryTestCaseView(APITestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',password='testpassword')
        self.country=Country.objects.create(name='Test Country')

    def test_get_country(self):
        resposne=self.client.get("/country/countries/")
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)
        self.assertEqual(len(resposne.data),1)

    def test_post_country(self):
        data={
            "name":"India",
            "createdby":self.user.id,
            "updatedby":self.user.id
        }
        resposne=self.client.post("/country/countries/",data)
        self.assertEqual(resposne.status_code,status.HTTP_201_CREATED)
        self.assertEqual(resposne.data['name'],'India')

    def test_single_get_country_by_id(self):
        resposne=self.client.get(f"/country/countries/?country_id={self.country.country_id}")
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)
        self.assertEqual(resposne.data[0]['name'],'Test Country')

    def test_single_get_country_by_name(self):
        response=self.client.get(f'/country/countries/?country_name=Test Country')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Test Country')

    def test_single_get_query_parameter(self):
        response=self.client.get(f'/country/countries/?abc=123')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],'Invalid Parameter')

    def test_single_get_not_found(self):
        response=self.client.get(f'/country/countries/?country_id=999')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],'No Country found matching your search criteria.')

    def test_put_country(self):
        # import pdb
        # pdb.set_trace()
        data={
            "name":"Brazil",
            "createdby":self.user.id,
            "updatedby":self.user.id
        }
        resposne=self.client.put(f"/country/countries/update/{self.country.country_id}/",data,format='json')
        self.assertEqual(resposne.status_code,status.HTTP_200_OK)
        self.assertEqual(resposne.data['name'],'Brazil')

    def test_delete_country(self):
        response=self.client.delete(f'/country/countries/delete/{self.country.country_id}/')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Country.objects.filter(country_id=self.country.country_id).exists())
        