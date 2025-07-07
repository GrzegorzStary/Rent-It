from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from items.models import Product

# Create your views here.

# Here we will render profile page later on
def profile_view(request):
    user = request.user
    profile = user.profile
    items = request.user.products.all()
    
    context = {
        'profile': profile,
        'items': items,
    }
    
    return render(request, 'profiles/profile.html', context)