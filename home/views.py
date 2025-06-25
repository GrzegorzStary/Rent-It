from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Items

# Create your views here.

class Index(TemplateView):
    template_name = 'home/index.html'

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Items.objects.filter(name__icontains=query)
        
    return render(request, 'search_results.html', {
        query: query,
        'results': results
    })