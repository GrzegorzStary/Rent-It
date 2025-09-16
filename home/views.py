from django.shortcuts import render
from django.views.generic import TemplateView
from items.models import Product


class Index(TemplateView):
    template_name = "home/index.html"


def search_view(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(
        request,
        "home/search_results.html",
        {"query": query, "results": results},
    )


def home(request):
    recent_products = Product.objects.order_by("-id")[:12]
    return render(
        request,
        "home/index.html",
        {"recent_products": recent_products},
    )


def privacy_policy(request):
    return render(request, "home/privacy_policy.html")


def terms_of_service(request):
    return render(request, "home/terms_of_service.html")


def faq(request):
    return render(request, "home/faq.html")
