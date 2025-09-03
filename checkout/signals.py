from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import OrderLineItem


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Ensure order totals stay accurate when a line item is deleted.
    """
    instance.order.update_total()
