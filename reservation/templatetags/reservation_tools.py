from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.simple_tag
def calc_subtotal(price, duration, deposit):
    """
    Calculate the total: (price * duration + deposit) + 10% site fee.
    """
    try:
        price = Decimal(price)
        duration = Decimal(duration)
        deposit = Decimal(deposit)
        subtotal = price * duration + deposit
        site_fee = subtotal * Decimal("0.10")
        total = subtotal + site_fee
        return total.quantize(Decimal("0.01"))
    except (TypeError, ValueError, InvalidOperation):
        return Decimal("0.00")
