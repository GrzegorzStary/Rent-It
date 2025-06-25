from django.urls import path
from .views import Index, search_view

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('search/', search_view, name='search'),
]