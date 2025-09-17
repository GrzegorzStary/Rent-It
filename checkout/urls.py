from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path("", views.checkout, name="checkout"),
    # Page after successful rental
    path("checkout_success/<order_number>/", views.checkout_success, name="checkout_success",
    ),
    # Cache checkout session data for Stripe
    path("cache_checkout_data/", views.cache_checkout_data, name="cache_checkout_data"),
    # Stripe webhook endpoint
    path("wh/", webhooks.webhook, name="checkout_webhook"),
]
