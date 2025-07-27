from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, duration):
    """
    Calculate the total: price * duration + 5% site fee.
    """
    try:
        price = Decimal(price)
        duration = Decimal(duration)
        subtotal = price * duration
        site_fee = subtotal * Decimal("0.05")
        total = subtotal + site_fee
        return total.quantize(Decimal("0.01"))  # round to 2 decimal places
    except (TypeError, ValueError, InvalidOperation):
        return Decimal("0.00")
