from django.shortcuts import render

# Create your views here.


# Here we will render items page later on
def items_view(request):
    
    return render(request, 'items/items.html', {})
