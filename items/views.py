from django.shortcuts import render
from .models import Product

# Create your views here.


# Here we will render items page later on
def items_view(request):
    
    products = Product.objects.all()

    context = {'products': products}

    return render(request, 'items/items.html', context)
