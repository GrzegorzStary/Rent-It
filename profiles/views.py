from django.shortcuts import render

# Create your views here.

# Here we will render profile page later on
def profile_view(request):
    return render(request, 'profiles/profile.html', {})