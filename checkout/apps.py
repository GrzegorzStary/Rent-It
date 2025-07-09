from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
    verbose_name = 'Checkout & Orders'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import checkout.signals
