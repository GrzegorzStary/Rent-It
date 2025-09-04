# items/views.py
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ProductForm
from .models import Product, ProductImage
from reservation.models import Reservation


# List/browse items (only manually listed ones)
def items_view(request):
    query = None
    sort = request.GET.get('sort')

    # Only show items that owners marked as listed/available
    products = Product.objects.filter(is_listed=True)

    # Search
    if request.GET.get('q') is not None:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('items'))
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

    # Sorting
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


# Item detail
def items_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # If the listing is manually hidden, do not let non owners view it
    if not product.is_listed and (not request.user.is_authenticated or product.user != request.user):
        messages.info(request, "This listing is currently unavailable.")
        return redirect('items')

    # Build calendar of dates that are already reserved
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
        # Template show a banner if owner is viewing a hidden item
        'is_hidden_owner_view': (not product.is_listed and request.user.is_authenticated and product.user == request.user),
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
            messages.error(request, 'Please correct the errors below.')
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
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect(reverse('items'))

    context = {'product': product}
    return render(request, 'items/delete_item.html', context)

@login_required
def add_to_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Prevent adding hidden/unlisted items to basket
    if not product.is_listed and product.user != request.user:
        messages.error(request, 'This item is currently unavailable.')
        return redirect('item_detail', pk=pk)

    basket = request.session.get('basket', {})
    pk_str = str(pk)
    if pk_str in basket:
        basket[pk_str] += 1
    else:
        basket[pk_str] = 1
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
            messages.success(request, 'Listing created!')
            return redirect('item_detail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
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


# Owner can manually toggle visibility of a listing
@require_POST
@login_required
def toggle_listing(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    product.is_listed = not product.is_listed
    product.save(update_fields=['is_listed'])

    if product.is_listed:
        messages.success(request, f'Listing enabled for “{product.name}”.')
    else:
        messages.warning(request, f'Listing disabled for “{product.name}”.')

    # Redirect back to where the owner came from, or to their listed items page
    return redirect(request.POST.get('next') or 'listed_items')
