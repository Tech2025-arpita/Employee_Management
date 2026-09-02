from django.db import models

class Store(models.Model):
    '''Store Model'''
    store_id = models.BigAutoField("StoreID", primary_key=True)
    store_name = models.CharField("StoreName", max_length=255, unique=True)
    store_code = models.CharField("StoreCode",max_length=20,unique=True,editable=False)
    store_add = models.CharField("Description", max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True) 

    def save(self, *args, **kwargs):

        if not self.store_code:
            self.store_code = self.store_name.upper()[:16] #generate letter

        super().save(*args, **kwargs)

        if self.store_code == self.store_name.upper()[:16]:
            self.store_code = f"{self.store_name.upper()[:16]}{self.store_id:03d}" #generate no with that
            super().save(update_fields=["store_code"])

    class Meta:
        db_table = 'CO_STORES'