# profiles/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch

from .models import Profile
from .forms import ProfileForm
from items.models import Product
from checkout.models import Order, OrderLineItem


@login_required
def profile_view(request):
    """
    Displays the user's profile information.
    """
    profile = request.user.profile
    return render(request, 'profiles/profile.html', {
        'profile': profile,
    })


@login_required
def edit_profile(request):
    """
    Allows the user to edit their profile details.
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {
        'form': form,
    })


@login_required
def listed_items(request):
    """
    Displays a separate page with all products listed by the logged-in user.
    """
    items = request.user.products.all()  # assumes Product.user has related_name="products"
    return render(request, 'profiles/listed_items.html', {
        'items': items,
    })


@login_required
def rented_items(request):
    """
    Shows all orders placed by the logged-in user (their rentals).
    Assumes:
      - Order has a FK to Profile named `user_profile`
      - OrderLineItem has related_name="lineitems" back to Order
      - OrderLineItem has FK `product` -> Product, and Product has related images via `images`
    """
    profile = request.user.profile

    orders = (
        Order.objects
        .filter(user_profile=profile)
        .prefetch_related(
            Prefetch(
                'lineitems',
                queryset=OrderLineItem.objects
                    .select_related('product', 'order')
                    .prefetch_related('product__images', 'product__user')
            )
        )
        .order_by('-date')
    )

    return render(request, 'profiles/rented_items.html', {
        'orders': orders,
    })
