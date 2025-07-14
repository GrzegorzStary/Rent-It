from django.urls import path
from .views import Index, search_view, privacy_policy, terms_of_service, faq
from home.views import home

urlpatterns = [
    path('home/', home, name='home'),
    path('search/', search_view, name='search'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('faq/', faq, name='faq'),
]