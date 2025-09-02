from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
from items.models import Product

FEE_RATE = Decimal("0.10")  # 10% fee

def checkout_context(request):
    """
    Checkout-only context: calculates totals using request.session['checkout']
    """
    checkout = request.session.get('checkout', {})

    checkout_items = []
    checkout_total = Decimal("0.00")
    deposit_total = Decimal("0.00")
    checkout_product_count = 0

    for item_id, item_data in checkout.items():
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):
            duration = item_data
        else:
            duration = item_data.get("duration", 1)

        subtotal = product.price * Decimal(duration)
        deposit = product.deposit or Decimal("0.00")

        checkout_total += subtotal
        deposit_total += deposit
        checkout_product_count += 1

        checkout_items.append({
            'product': product,
            'subtotal': subtotal,
            'deposit': deposit,
            'user': product.user,
            'image': product.images.first().image.url if product.images.exists() else None,
        })

    checkout_grand_total = (checkout_total + deposit_total).quantize(Decimal("0.01"))

    return {
        'checkout_items': checkout_items,
        'checkout_total': checkout_total.quantize(Decimal("0.01")),
        'deposit_total': deposit_total.quantize(Decimal("0.01")),
        'checkout_grand_total': checkout_grand_total,
        'checkout_product_count': checkout_product_count,
    }
