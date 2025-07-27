from decimal import Decimal
from django.shortcuts import get_object_or_404
from items.models import Product

def cart_context(request):
    """
    Make bag and/or checkout contents available globally.
    """
    bag = request.session.get('bag', {})
    checkout = request.session.get('checkout', {})
    bag_total = Decimal("0.00")
    bag_items = []
    bag_product_count = 0

    for item_id, duration in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = (product.price * duration) * Decimal("1.05")  # include 5% fee
        bag_total += subtotal
        bag_product_count += 1

        bag_items.append({
            'item_id': item_id,
            'product': product,
            'duration': duration,
            'subtotal': subtotal,
        })

    # Checkout logic
    checkout_items = []
    checkout_total = Decimal("0.00")
    deposit_total = Decimal("0.00")
    checkout_product_count = 0

    for item_id, item_data in checkout.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = product.price
        deposit = product.deposit
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

    context = {
        # bag
        'bag_items': bag_items,
        'bag_total': bag_total.quantize(Decimal("0.01")),
        'bag_product_count': bag_product_count,
        'grand_total': bag_total.quantize(Decimal("0.01")),
        # checkout
        'checkout_items': checkout_items,
        'checkout_total': checkout_total,
        'deposit_total': deposit_total,
        'checkout_grand_total': checkout_total + deposit_total,
        'checkout_product_count': checkout_product_count,
    }

    return context
