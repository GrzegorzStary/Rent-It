from django.contrib import admin
from .models import Category, Product

# Register your models here.
    # This is displaying friendly name in our admin panel
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    # This creating additional ordering options on admin panel
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)
    
admin.site.register(Category , CategoryAdmin)
admin.site.register(Product , ProductAdmin)