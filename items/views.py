from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


# Here we will render items page later on
def items_view(request):
    
    products = Product.objects.all()

    context = {'products': products}

    return render(request, 'items/items.html', context)


"""This view will render item detail page of individual product."""
def items_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'items/item_detail.html', context)