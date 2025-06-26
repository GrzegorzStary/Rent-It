from django.shortcuts import render

# Create your views here.

# Here we will render reservation page later on
def reservation_view(request):
    return render(request, 'reservation/reservation.html', {})