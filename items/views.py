# items/views.py
from datetime import timedelta
from math import radians, sin, cos, asin, sqrt

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import ProductForm
from .models import Product, ProductImage
from reservation.models import Reservation


# Distance helpers
EARTH_RADIUS_KM = 6371.0088

def haversine_km(lat1, lng1, lat2, lng2):
    """Accurate great-circle distance in kilometers."""
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))

def bbox_around(lat, lng, km):
    """Quick bounding box for prefiltering."""
    lat_delta = km / 110.574  # ~km per degree latitude
    # protect cos() near poles
    lng_delta = km / (111.320 * max(0.0001, cos(radians(lat))))
    return (lat - lat_delta, lat + lat_delta, lng - lng_delta, lng + lng_delta)


# List/browse items (only manually listed ones)
def items_view(request):
    query = None
    sort = request.GET.get('sort')
    max_km_param = request.GET.get('max_km')  # e.g. max_km=10
    radius_enabled = False
    user_lat = user_lng = None

    # Base queryset: only listed/available
    products = Product.objects.filter(is_listed=True)

    # Search
    if request.GET.get('q') is not None:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('items'))
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

    # Optional "near me" radius filter
    if request.user.is_authenticated and max_km_param:
        try:
            max_km = float(max_km_param)
        except (TypeError, ValueError):
            max_km = 10.0
        profile = getattr(request.user, 'profile', None)
        if profile and profile.lat is not None and profile.lng is not None:
            user_lat, user_lng = float(profile.lat), float(profile.lng)
            lat_min, lat_max, lng_min, lng_max = bbox_around(user_lat, user_lng, max_km)
            # Prefilter fast by bounding box on owners' profile coordinates
            products = (
                products
                .select_related('user__profile')
                .filter(
                    user__profile__lat__gte=lat_min,
                    user__profile__lat__lte=lat_max,
                    user__profile__lng__gte=lng_min,
                    user__profile__lng__lte=lng_max,
                )
            )
            radius_enabled = True
        else:
            messages.info(request, "Add a valid postcode to your profile to use the 'near me' filter.")

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

    product_list = list(products)

    # If radius filter is active, compute precise distance via Haversine and trim to <= max_km
    if radius_enabled and user_lat is not None and user_lng is not None:
        filtered = []
        # Use same max_km as parsed above; default 10 if parsing failed
        try:
            max_km_val = float(max_km_param)
        except (TypeError, ValueError):
            max_km_val = 10.0

        for p in product_list:
            prof = getattr(p.user, 'profile', None)
            if not prof or prof.lat is None or prof.lng is None:
                continue
            dist = haversine_km(user_lat, user_lng, float(prof.lat), float(prof.lng))
            if dist <= max_km_val:
                p.distance_km = round(dist, 2)
                filtered.append(p)

        # Sort "near me" results by distance by default (unless an explicit price/name sort was chosen)
        if sort in (None, '', 'None_None'):
            filtered.sort(key=lambda x: getattr(x, 'distance_km', 9e9))
        product_list = filtered

    context = {
        'products': product_list,
        'search_term': query,
        'current_sorting': sort if sort else 'None_None',
        'radius_active': radius_enabled,
        'max_km': max_km_param or '',
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

    # Distance to viewer display on detail page
    viewer_distance_km = None
    if request.user.is_authenticated:
        prof = getattr(request.user, 'profile', None)
        owner_prof = getattr(product.user, 'profile', None)
        if prof and owner_prof and prof.lat and prof.lng and owner_prof.lat and owner_prof.lng:
            viewer_distance_km = round(
                haversine_km(float(prof.lat), float(prof.lng), float(owner_prof.lat), float(owner_prof.lng)),
                2
            )

    context = {
        'product': product,
        'unavailable_dates': unavailable_dates,
        'viewer_distance_km': viewer_distance_km,
        # Template shows a banner if owner is viewing a hidden item
        'is_hidden_owner_view': (not product.is_listed and request.user.is_authenticated and product.user == request.user),
    }
    return render(request, 'items/item_detail.html', context)


@login_required
@transaction.atomic
def edit_item(request, pk):
    """
    Superusers can edit ANY item.
    Regular users can edit ONLY their own item.
    """
    # Build a performant base queryset
    base_qs = Product.objects.select_related("user", "category").prefetch_related("images")

    # Fetch object with proper permissions
    if request.user.is_superuser:
        item = get_object_or_404(base_qs, pk=pk)
    else:
        item = get_object_or_404(base_qs, pk=pk, user=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=item)
        files = request.FILES.getlist("images")  # multiple extra images

        if form.is_valid():
            item = form.save()

            # Save additional images
            for f in files:
                if f:
                    ProductImage.objects.create(product=item, image=f)

            messages.success(request, "Item updated successfully!")
            return redirect("item_detail", pk=item.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=item)

    existing_images = item.images.all()

    return render(
        request,
        "items/edit_item.html",
        {
            "form": form,
            "item": item,
            "existing_images": existing_images,
        },
    )



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Product


@login_required
def delete_item(request, pk):
    # Superuser: fetch by pk; Regular user: fetch by pk + owner
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('items')  # Redirect to item list

    # Show confirm page
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


# Optional dedicated "near me" page (10 km by default)
@login_required
def nearby_items(request):
    """
    Separate endpoint that always applies the radius filter.
    """
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.lat is None or profile.lng is None:
        messages.info(request, "Add a valid postcode to your profile to see nearby items.")
        return redirect('items')

    try:
        max_km = float(request.GET.get('max_km', 10))
    except (TypeError, ValueError):
        max_km = 10.0

    user_lat, user_lng = float(profile.lat), float(profile.lng)
    lat_min, lat_max, lng_min, lng_max = bbox_around(user_lat, user_lng, max_km)

    qs = (
        Product.objects.filter(is_listed=True)
        .select_related('user__profile')
        .filter(
            user__profile__lat__gte=lat_min,
            user__profile__lat__lte=lat_max,
            user__profile__lng__gte=lng_min,
            user__profile__lng__lte=lng_max,
        )
    )

    results = []
    for p in qs:
        owner_prof = getattr(p.user, 'profile', None)
        if owner_prof and owner_prof.lat is not None and owner_prof.lng is not None:
            d = haversine_km(user_lat, user_lng, float(owner_prof.lat), float(owner_prof.lng))
            if d <= max_km:
                p.distance_km = round(d, 2)
                results.append(p)

    results.sort(key=lambda x: x.distance_km)

    return render(request, 'items/nearby.html', {
        'items': results,
        'origin_postcode': profile.postal_code,
        'max_km': int(max_km),
    })
