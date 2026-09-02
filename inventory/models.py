from django.db import models
from product.models import Product
from store.models import Store

class Inventory(models.Model):
    '''Inventory Model'''
    inv_id=models.BigAutoField("InventoryID", primary_key=True)
    product=models.ForeignKey(Product,verbose_name="Product",on_delete=models.CASCADE,related_name="inventories")
    store =models.ForeignKey(Store,verbose_name="Store",on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     if self.quantity < 0:
    #         self.quantity = abs(self.quantity)

    #     super().save(*args, **kwargs)

    class Meta:
        db_table="inventory"

    def __str__(self):
        return f"{self.product.product_name} - {self.store.store_name}"