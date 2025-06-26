from django.shortcuts import render

# Create your views here.

# Her we will render checkout page in later on

def checkout_view(request):

    return render(request, 'checkout/checkout.html', {})