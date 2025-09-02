from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
from items.models import Product

FEE_RATE = Decimal("0.10")  # 10% site fee forwarded
DATE_FMT = "%d/%m/%Y"       # parse UK format

def checkout_context(request):
    """
    Checkout-only context: calculates totals using request.session['checkout']
    """
    checkout = request.session.get('checkout', {})

    checkout_items = []
    subtotal = Decimal("0.00")
    deposit_total = Decimal("0.00")
    checkout_product_count = 0

    for item_id, item_data in checkout.items():
        product = get_object_or_404(Product, pk=item_id)

        start_date = item_data.get("start_date")
        end_date = item_data.get("end_date")

        try:
            duration = (datetime.strptime(end_date, DATE_FMT).date() - datetime.strptime(start_date, DATE_FMT).date()).days
            duration = max(duration, 1)
        except Exception:
            duration = item_data.get("duration", 1)

        item_subtotal = product.price * Decimal(duration)
        deposit = product.deposit or Decimal("0.00")

        subtotal += item_subtotal
        deposit_total += deposit
        checkout_product_count += 1

        checkout_items.append({
            'product': product,
            'subtotal': item_subtotal,
            'deposit': deposit,
            'duration': duration,
            'start_date': start_date,
            'end_date': end_date,
            'user': product.user,
            'image': product.images.first().image.url if product.images.exists() else None,
        })

    site_fee = (subtotal * FEE_RATE).quantize(Decimal("0.01"))
    checkout_grand_total = (subtotal + deposit_total + site_fee).quantize(Decimal("0.01"))

    return {
        'checkout_items': checkout_items,
        'checkout_total': subtotal.quantize(Decimal("0.01")),
        'deposit_total': deposit_total.quantize(Decimal("0.01")),
        'site_fee': site_fee,
        'checkout_grand_total': checkout_grand_total,
        'checkout_product_count': checkout_product_count,
    }
