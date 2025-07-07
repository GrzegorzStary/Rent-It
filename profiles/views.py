from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from items.models import Product
from django.contrib import messages
from .forms import ProfileForm


#This view handles the shection where user can edit his profile.
@login_required
def profile_view(request):
    profile = request.user.profile
    items = request.user.products.all()  # Get all items associated with the user's profile
    return render(request, 'profiles/profile.html', {
        'profile': profile,
        'items': items,
    })

@login_required
def edit_profile(request):
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

    return render(request, 'profiles/edit_profile.html', {'form': form})

