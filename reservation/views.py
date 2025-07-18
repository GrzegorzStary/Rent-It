from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime
from items.models import Product


def view_bag(request):
    """Render the rental bag page with items from the session"""
    bag = request.session.get('bag', {})
    bag_items = []

    for item_id, duration in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        bag_items.append({
            'item_id': item_id,
            'product': product,
            'duration': duration,
        })

    context = {
        'bag_items': bag_items,
    }

    return render(request, 'reservation/reservation.html', context)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from items.models import Product


def add_to_bag(request, item_id):
    """
    Add an item to the rental bag with start & end dates (or fallback to duration=1).
    """
    product = get_object_or_404(Product, pk=item_id)

    bag = request.session.get('bag', {})

    # Get start and end dates or fallback to duration
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    redirect_url = request.POST.get('redirect_url', '/')

    # min duration
    duration = 1

    if start_date and end_date:
        try:
            # Parse dates from the format dd/mm/yyyy
            s = datetime.strptime(start_date, "%d/%m/%Y")
            e = datetime.strptime(end_date, "%d/%m/%Y")
            delta = (e - s).days
            duration = max(delta, 1)  # min 1 day
        except Exception:
            messages.warning(request, "Invalid dates selected — defaulting to 1 day.")

    else:
        # Check if `duration` is explicitly sent
        duration = int(request.POST.get('duration', 1))

    # store string key
    item_id_str = str(item_id)

    if item_id_str in bag:
        bag[item_id_str] += duration
        messages.success(
            request,
            f'Updated {product.name} rental duration to {bag[item_id_str]} day(s).'
        )
    else:
        bag[item_id_str] = duration
        messages.success(
            request,
            f'Added {product.name} to your rental bag for {duration} day(s).'
        )

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the rental duration for a specific item in the bag"""
    product = get_object_or_404(Product, pk=item_id)

    duration = int(request.POST.get('duration', 1))

    bag = request.session.get('bag', {})

    if duration > 0:
        bag[item_id] = duration
        messages.success(
            request,
            f'Updated {product.name} rental duration to {duration} day(s).'
        )
    else:
        bag.pop(item_id, None)
        messages.success(
            request,
            f'Removed {product.name} from your rental bag.'
        )

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove an item completely from the rental bag"""
    product = get_object_or_404(Product, pk=item_id)

    try:
        bag = request.session.get('bag', {})
        bag.pop(item_id, None)
        messages.success(
            request,
            f'Removed {product.name} from your rental bag.'
        )
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

