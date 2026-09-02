from django.db import models
from django.utils.text import slugify 

class Category(models.Model):
    '''Category Model'''
    category_id = models.BigAutoField("CategoryID", primary_key=True)
    name = models.CharField("CategoryName", max_length=255)
    slug = models.SlugField("CategorySlug", max_length=255, unique=True)
    description = models.CharField("Description", max_length=255, blank=True, null=True)
    parent_id= models.ForeignKey("self",verbose_name="ParentCategory",on_delete=models.CASCADE,
                               null=True,blank=True,related_name="children")

    class Meta:
        db_table = "category"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name