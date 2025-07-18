import uuid
from django.db import models
from django.contrib.auth.models import User


# Category model
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name


# Product model
class Product(models.Model):
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name='products'
    )
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='products'
    )
    sku = models.CharField(max_length=254, unique=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deposit = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# This is creating random SKU for each product if not provided number of characters is 10 so that stays unique.
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = str(uuid.uuid4()).replace('-', '')[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ProductImage model for multiple images per product
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    