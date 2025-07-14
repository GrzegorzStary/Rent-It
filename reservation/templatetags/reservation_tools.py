from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, duration):
    """
    Calculate the subtotal, price and duration.
    """
    try:
        # Convert to Decimal for precision, if using money
        price = Decimal(price)
        duration = Decimal(duration)
        return price * duration
    except (TypeError, ValueError, InvalidOperation):
        return Decimal("0.00")
