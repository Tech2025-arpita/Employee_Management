from django.test import SimpleTestCase
from django.urls import reverse,resolve
from country.views import(
    CountryListCreate,
    CountryUpdateView,
    CountryDeleteiew
    )
class CountryUrlTest(SimpleTestCase):
    def test_country_get_create_url(self):
        url=reverse('country_read_create')
        self.assertEqual(resolve(url).func.view_class,CountryListCreate)
    def test_country_update_url(self):
        url=reverse('countries_update',kwargs={"pk":1})
        self.assertEqual(resolve(url).func.view_class,CountryUpdateView)
    def test_country_delete_url(self):
        url=reverse('countries_delete',kwargs={"pk":1})
        self.assertEqual(resolve(url).func.view_class,CountryDeleteiew)