from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from items.models import Product
from reservation.models import Reservation
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

DATE_FMT = "%Y-%m-%d"


def _parse_duration_from_dates(start_date, end_date):
    try:
        s = datetime.strptime(start_date, "%d/%m/%Y").date()
        e = datetime.strptime(end_date, "%d/%m/%Y").date()
        days = (e - s).days
        return max(days, 1)
    except Exception as e:
        print("DATE PARSE ERROR >>>", e)
        return 1


@login_required
def view_bag(request):
    bag = request.session.get('bag', {})
    bag_items = []

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):
            item_data = {"duration": item_data}

        duration = item_data.get('duration', 1)
        start_date = item_data.get('start_date')
        end_date = item_data.get('end_date')

        # Recalculate duration
        parsed_duration = _parse_duration_from_dates(start_date, end_date)
        if parsed_duration:
            duration = parsed_duration

        subtotal = float(product.price) * int(duration)

        user_reservation = (
            {"start_date": start_date, "end_date": end_date}
            if start_date and end_date else None
        )

        bag_items.append({
            'item_id': item_id,
            'product': product,
            'duration': duration,
            'start_date': start_date,
            'end_date': end_date,
            'subtotal': subtotal,
            'deposit': product.deposit,
            'user_reservation': user_reservation,
        })

    bag_total = sum(item['subtotal'] for item in bag_items)
    deposit_total = sum(float(item['deposit'] or 0) for item in bag_items)
    site_fee = bag_total * 0.10
    grand_total = bag_total + site_fee + deposit_total

    context = {
        'bag_items': bag_items,
        'bag_total': round(bag_total, 2),
        'site_fee': round(site_fee, 2),
        'deposit': round(deposit_total, 2),
        'grand_total': round(grand_total, 2),
        'today': date.today(),
    }

    return render(request, 'reservation/reservation.html', context)


@login_required
def add_to_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    item_key = str(item_id)

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    redirect_url = request.POST.get('redirect_url', '/')

    duration = _parse_duration_from_dates(start_date, end_date)
    if duration is None:
        try:
            duration = int(request.POST.get('duration', 1))
        except Exception:
            duration = 1

    bag[item_key] = {
        "start_date": start_date,
        "end_date": end_date,
        "duration": duration,
    }

    messages.success(
        request,
        f'Added or updated {product.name} in your rental bag '
        f'for {duration} day(s).'
    )

    request.session['bag'] = bag
    request.session.modified = True
    return redirect(redirect_url)


@login_required
def adjust_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    item_key = str(item_id)

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    duration = _parse_duration_from_dates(start_date, end_date)
    if duration is None:
        try:
            duration = int(request.POST.get('duration', 1))
        except Exception:
            duration = 1

    bag[item_key] = {
        "start_date": start_date,
        "end_date": end_date,
        "duration": duration,
    }

    messages.success(
        request,
        f'Updated {product.name} rental duration to {duration} day(s).'
    )

    request.session['bag'] = bag
    request.session.modified = True
    return redirect(reverse('reservation:view_bag'))


@login_required
@require_POST
def remove_from_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    try:
        bag = request.session.get('bag', {})
        bag.pop(str(item_id), None)
        request.session['bag'] = bag
        messages.success(
            request,
            f'Removed {product.name} from your rental bag.'
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
