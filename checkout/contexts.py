from decimal import Decimal
from django.shortcuts import get_object_or_404
from items.models import Product

def checkout_contents(request):
    """
    Return checkout session data: items, total, grand_total etc.
    """
    checkout = request.session.get('checkout', {})
    total = Decimal('0.00')
    deposit_total = Decimal('0.00')
    product_count = 0
    checkout_items = []

    for item_id, item_data in checkout.items():
        # Checking if the item exists in the database if not 404
        product = get_object_or_404(Product, id=item_id)

        # calculate subtotal and deposit
        price = product.price
        deposit = product.deposit
        subtotal = price

        total += subtotal
        deposit_total += deposit
        product_count += 1

        checkout_items.append({
            'product': product,
            'subtotal': subtotal,
            'deposit': deposit,
            'user': product.user,
            'image': product.images.first().image.url if product.images.exists() else None,
        })

    grand_total = total + deposit_total  # need to include delivefry fee if there is any (later)

    context = {
        'checkout_items': checkout_items,
        'total': total,
        'deposit_total': deposit_total,
        'grand_total': grand_total,
        'product_count': product_count,
    }

    return context
