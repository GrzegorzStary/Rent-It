from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, ProductImage
from reservation.models import Reservation
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.http import JsonResponse
from datetime import timedelta

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

    booked_ranges = Reservation.objects.filter(product=product).values('start_date', 'end_date')

    unavailable_dates = []
    for r in booked_ranges:
        current = r['start_date']
        while current <= r['end_date']:
            unavailable_dates.append(current.strftime('%d-%m-%Y'))
            current += timedelta(days=1)

    context = {
        'product': product,
        'unavailable_dates': unavailable_dates,
    }

    return render(request, 'items/item_detail.html', context)


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            # Save additional images if any
            for f in files:
                ProductImage.objects.create(product=item, image=f)
            messages.success(request, 'Item updated successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ProductForm(instance=item)
        
# Get existing images for the item
    existing_images = item.images.all()
    return render(request, 'items/edit_item.html', {
        'form': form,
        'item': item,
        'existing_images': existing_images,
    })

@login_required
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

@login_required
def add_to_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = request.session.get('basket', {})
    if pk in basket:
        basket[pk] += 1
    else:
        basket[pk] = 1
    request.session['basket'] = basket
    messages.success(request, f'Added {product.name} to your basket!')
    return redirect(reverse('item_detail', args=[pk]))

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            return redirect('user_profile')
    else:
        form = ProductForm()
    return render(request, 'items/create_listing.html', {'form': form})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id, product__user=request.user)
    product_id = image.product.id
    image.delete()
    messages.success(request, "Image deleted.")
    return redirect('edit_item', pk=product_id)
