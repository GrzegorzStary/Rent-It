from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
from items.models import Product

FEE_RATE = Decimal("0.10")  # 10% fee

def cart_context(request):
    """
    Checkout contents available globally.
    """
    bag = request.session.get('bag', {})
    checkout = request.session.get('checkout', {})

    # BAG 
    bag_items = []
    bag_total = Decimal("0.00") 
    bag_deposit_total = Decimal("0.00")    
    bag_product_count = 0

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Defaults
        start_date = None
        end_date = None

        if isinstance(item_data, int):
            duration = item_data
        else:
            start_date = item_data.get("start_date")
            end_date = item_data.get("end_date")

            # Calculate duration safely
            try:
                if start_date and end_date:
                    start = datetime.strptime(start_date, "%Y-%m-%d")
                    end = datetime.strptime(end_date, "%Y-%m-%d")
                    duration = max((end - start).days, 1)
                else:
                    duration = 1
            except Exception:
                duration = 1

        base = product.price * Decimal(duration)
        fee = (base * FEE_RATE)
        subtotal = base + fee    

        bag_total += subtotal
        bag_deposit_total += (product.deposit or Decimal("0.00"))
        bag_product_count += 1

        bag_items.append({
            'item_id': item_id,
            'product': product,
            'duration': duration,
            'subtotal': subtotal,
            'fee': fee,
            'deposit': product.deposit,
            'start_date': start_date,
            'end_date': end_date,
        })

    grand_total = (bag_total + bag_deposit_total).quantize(Decimal("0.01"))

    # CHECKOUT 
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

    context = {
        # BAG
        'bag_items': bag_items,
        'bag_total': bag_total.quantize(Decimal("0.01")),
        'bag_deposit_total': bag_deposit_total.quantize(Decimal("0.01")),
        'bag_product_count': bag_product_count,
        'grand_total': grand_total,

        # CHECKOUT
        'checkout_items': checkout_items,
        'checkout_total': checkout_total.quantize(Decimal("0.01")),
        'deposit_total': deposit_total.quantize(Decimal("0.01")),
        'checkout_grand_total': checkout_grand_total,
        'checkout_product_count': checkout_product_count,
    }

    return context
