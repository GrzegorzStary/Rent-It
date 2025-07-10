from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404
)
from django.contrib import messages

from items.models import Product


def view_bag(request):
    """ Render the rental bag page """
    return render(request, 'reservation/reservation.html')


def add_to_bag(request, item_id):
    """ Add an item to the rental bag with specified duration """

    product = get_object_or_404(Product, pk=item_id)

    duration = int(request.POST.get('duration', 1))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size', None)

    bag = request.session.get('bag', {})

    if size:
        if item_id in bag:
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size] += duration
                messages.success(
                    request,
                    f'Updated {product.name} (Size: {size.upper()}) rental duration to '
                    f'{bag[item_id]["items_by_size"][size]} day(s)'
                )
            else:
                bag[item_id]['items_by_size'][size] = duration
                messages.success(
                    request,
                    f'Added {product.name} (Size: {size.upper()}) to your rental bag'
                )
        else:
            bag[item_id] = {'items_by_size': {size: duration}}
            messages.success(
                request,
                f'Added {product.name} (Size: {size.upper()}) to your rental bag'
            )
    else:
        if item_id in bag:
            bag[item_id] += duration
            messages.success(
                request,
                f'Updated {product.name} rental duration to {bag[item_id]} day(s)'
            )
        else:
            bag[item_id] = duration
            messages.success(
                request,
                f'Added {product.name} to your rental bag'
            )

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the rental duration for a specific item in the bag """

    product = get_object_or_404(Product, pk=item_id)

    duration = int(request.POST.get('duration', 1))
    size = request.POST.get('product_size', None)

    bag = request.session.get('bag', {})

    if size:
        if duration > 0:
            bag[item_id]['items_by_size'][size] = duration
            messages.success(
                request,
                f'Updated {product.name} (Size: {size.upper()}) rental duration to '
                f'{bag[item_id]["items_by_size"][size]} day(s)'
            )
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} (Size: {size.upper()}) from your rental bag'
            )
    else:
        if duration > 0:
            bag[item_id] = duration
            messages.success(
                request,
                f'Updated {product.name} rental duration to {bag[item_id]} day(s)'
            )
        else:
            bag.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} from your rental bag'
            )

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove an item completely from the rental bag """

    product = get_object_or_404(Product, pk=item_id)

    try:
        size = request.POST.get('product_size', None)
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} (Size: {size.upper()}) from your rental bag'
            )
        else:
            bag.pop(item_id)
            messages.success(
                request,
                f'Removed {product.name} from your rental bag'
            )

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
