from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    # Main checkout page where the user fills their details
    path('', views.checkout, name='checkout'),
    # Page to display after successful rental
    path('checkout_success/<order_number>/', 
         views.checkout_success, name='checkout_success'),
    # Cache checkout session data in Stripe
    path('cache_checkout_data/', 
         views.cache_checkout_data, name='cache_checkout_data'),
    # Stripe webhook endpoint for payment confirmation events
    path('wh/', webhook, name='checkout_webhook'),
]
