from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product
from django.db.models import Q
from django.contrib import messages

# Create your views here.


# Here we will render items page later on
def items_view(request):
    query = None
    products = Product.objects.all()

    if request.GET and 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('items'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = Product.objects.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'items/items.html', context)


"""This view will render item detail page of individual product."""
def items_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
    }

    return render(request, 'items/item_detail.html', context)