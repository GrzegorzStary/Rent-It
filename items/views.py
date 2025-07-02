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

def edit_item (request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.save()
        messages.success(request, 'Item updated successfully!')
        return redirect(reverse('items_detail', args=[pk]))

    context = {
        'product': product,
    }

    return render(request, 'items/edit_item.html', context)

def delete_item(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect(reverse('items'))

    context = {
        'product': product,
    }

    return render(request, 'items/delete_item.html', context)

def add_to_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = request.session.get('basket', {})
    if pk in basket:
        basket[pk] += 1
    else:
        basket[pk] = 1
    request.session['basket'] = basket
    messages.success(request, f'Added {product.name} to your basket!')
    return redirect(reverse('items_detail', args=[pk]))