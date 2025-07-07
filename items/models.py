import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Category models
class Category(models.Model):
    
    # This meta is changing wrong django spelling of plural name
    class Meta:
        verbose_name_plural = 'Categories'
            
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name
    
# Product models 
class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, on_delete=models.SET_NULL)
    # This is to link product with user who created it
    user = models.ForeignKey(
        'auth.User', null=True, on_delete=models.SET_NULL, related_name='products')
    sku = models.CharField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deposit = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True)
    image_url = models.URLField(max_length=1024, null=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Automatically generate SKU if not provided
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = str(uuid.uuid4()).replace('-', '')[:10]  # Generate a unique SKU
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name