from django.db import models
from brand.models import Brand
from category.models import Category
from store.models import Store

status=(
    ('A','Active'),
    ('I','Inactive'),
)

class Product(models.Model):
    product_id = models.BigAutoField("ProductID", primary_key=True)
    product_name=models.CharField("productName",blank=False,max_length=250)
    product_sku=models.CharField("productSku",max_length=30, unique=True, db_index=True)
    short_desc=models.CharField("ShortDescription", max_length=255, blank=True, null=True)
    long_desc=models.CharField("LongDescription", max_length=255, blank=True, null=True)
    product_status=models.CharField(max_length=1,choices=status,default="A")
    product_brand=models.ForeignKey(Brand,verbose_name="product_brand",on_delete=models.CASCADE)
    product_category=models.ForeignKey(Category,verbose_name="product_category",on_delete=models.CASCADE)
    product_price=models.DecimalField(max_digits=10,decimal_places=2)
    # product_store=models.ForeignKey(Store,verbose_name="product_store",on_delete=models.CASCADE) #Without do it command out we can ismpy do it null 

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.product_name

##Api payload shipment 
class ShipStationLabel(models.Model):
    label_id = models.CharField(max_length=100, unique=True)
    shipment_id = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)

    carrier_id = models.CharField(max_length=100)
    service_code = models.CharField(max_length=100)

    status = models.CharField(max_length=50)

    shipment_cost = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    label_format = models.CharField(max_length=20)

    label_pdf_url = models.URLField(max_length=500)

    tracking_url = models.URLField(max_length=500,null=True,blank=True)

    created_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = "shipstation_label"

    def __str__(self):
        return self.label_id