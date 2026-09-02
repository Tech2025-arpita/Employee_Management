from django.db import models

class Brand(models.Model):
    '''Brand Model'''
    brand_id = models.BigAutoField("BrandID", primary_key=True)
    brand_name = models.CharField("BrandName", max_length=255, unique=True)
    brand_code = models.CharField("BrandCode",max_length=20,unique=True,editable=False)
    brand_desc = models.CharField("Description", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.brand_code:
            self.brand_code = self.brand_name.upper()[:16]

        super().save(*args, **kwargs)

        if self.brand_code == self.brand_name.upper()[:16]:
            self.brand_code = f"{self.brand_name.upper()[:16]}{self.brand_id:03d}"
            super().save(update_fields=["brand_code"])