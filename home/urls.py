from django.urls import path
from .views import Index, search_view
from home.views import home

urlpatterns = [
    path('home/', home, name='home'),
    path('search/', search_view, name='search'),
]