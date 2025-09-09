from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
from items.models import Product

FEE_RATE = Decimal("0.10")   # 10% site fee
DATE_FMT = "%d/%m/%Y"        # UK format DD/MM/YYYY

def _parse_duration(item_data):
    """
    Prefer start/end dates; fall back to provided duration.
    """
    start = item_data.get("start_date")
    end   = item_data.get("end_date")

    
    if start and end:
        try:
            d_start = datetime.strptime(start, DATE_FMT).date()
            d_end   = datetime.strptime(end, DATE_FMT).date()
            days = (d_end - d_start).days
            return max(int(days), 1)
        except Exception:
            pass

    
    dur = item_data.get("duration", 1)
    try:
        return max(int(dur), 1)
    except (TypeError, ValueError):
        return 1


def checkout_context(request):
    """
    Build checkout summary from session['checkout'].
    """
    checkout = request.session.get('checkout', {}) or {}

    items = []
    rental_total  = Decimal("0.00")
    deposit_total = Decimal("0.00")
    product_count = 0

    for item_id, item_data in checkout.items():
        
        product = get_object_or_404(Product, pk=int(item_id))

        duration = _parse_duration(item_data)

        
        price   = getattr(product, 'price', None)
        price   = Decimal(price) if isinstance(price, (int, float, str)) else (price or Decimal("0.00"))

        deposit = getattr(product, 'deposit', None)
        deposit = Decimal(deposit) if isinstance(deposit, (int, float, str)) else (deposit or Decimal("0.00"))

        item_subtotal = (price * Decimal(duration))
        rental_total  += item_subtotal
        deposit_total += deposit
        product_count += 1

        
        img_url = None
        try:
            if product.images.exists():
                first_img = product.images.first()
                if first_img and getattr(first_img, "image", None):
                    img_url = first_img.image.url
        except Exception:
            img_url = None

        items.append({
            'product': product,
            'subtotal': item_subtotal.quantize(Decimal("0.01")),
            'deposit': deposit.quantize(Decimal("0.01")),
            'duration': duration,
            'start_date': item_data.get('start_date'),
            'end_date': item_data.get('end_date'),
            'user': getattr(product, 'user', None),
            'image': img_url,
        })

    site_fee = (rental_total * FEE_RATE).quantize(Decimal("0.01"))
    grand    = (rental_total + deposit_total + site_fee).quantize(Decimal("0.01"))

    return {
        'checkout_items': items,
        'checkout_total': rental_total.quantize(Decimal("0.01")),
        'deposit_total': deposit_total.quantize(Decimal("0.01")),
        'site_fee': site_fee,
        'checkout_grand_total': grand,
        'checkout_product_count': product_count,
    }
