from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

    # This is displaying friendly name in our admin panel
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    ordering = ('name',)
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # how many empty forms to show
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="75" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Preview"
        
    # This creating additional ordering options on admin panel
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
    )
    ordering = ('sku',)
    search_fields = ('name', 'description', 'category__name', 'sku')
    list_filter = ('category',)
    
    inlines = [ProductImageInline]
    
    def thumbnail(self,obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" width="50" />', first_image.image.url)
        return "No Image"
    
    thumbnail.short_description = "Image"
    