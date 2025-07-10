from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from items.models import Product
from .forms import ProfileForm


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
    items = request.user.products.all()  # Get all items associated with the user's profile
    return render(request, 'profiles/listed_items.html', {
        'items': items,
    })

