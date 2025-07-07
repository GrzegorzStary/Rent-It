from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

# Create your views here.


# Here we will render items page
def items_view(request):
    query = None
    sort = request.GET.get('sort')
    products = Product.objects.all()

    # Handle search functionality
    if request.GET.get('q'):
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('items'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

    # Handle sorting functionality
    if sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    elif sort == 'rating_asc':
        products = products.order_by('rating')
    elif sort == 'rating_desc':
        products = products.order_by('-rating')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'category_asc':
        products = products.order_by('category__name')
    elif sort == 'category_desc':
        products = products.order_by('-category__name')

    context = {
        'products': products,
        'search_term': query,
        'current_sorting': sort if sort else 'None_None',
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

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('user_profile')
    else:
        form = ProductForm()
    return render(request, 'items/create_listing.html', {'form': form})