from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .forms import OrderForm
from .models import Order, OrderLineItem
from items.models import Product
from profiles.forms import ProfileForm
from profiles.models import Profile
from checkout.checkout_context import checkout_context
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe
import json
from stripe.error import InvalidRequestError

DATE_FMT = "%d/%m/%Y"  # UK format


def cache_checkout_data(request):
    """
    Save checkout data into the PaymentIntent metadata for webhook recovery.
    """
    try:
        client_secret = request.POST.get('client_secret', '')
        pid = client_secret.split('_secret')[0] if client_secret else ''
        if not pid:
            return HttpResponse(content='Missing client_secret', status=400)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'checkout': json.dumps(request.session.get('checkout', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username if request.user.is_authenticated else 'anon',
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)


def _get_or_create_payment_intent(stripe_secret_key: str, amount_pennies: int, currency: str, session):
    """
    Reuse an existing PaymentIntent from the session if possible.
    Create a new one if amount changed or status isn’t reusable.
    """
    stripe.api_key = stripe_secret_key
    intent = None
    reusable_statuses = {'requires_payment_method', 'requires_confirmation', 'requires_action'}

    pi_info = session.get('stripe_pi')
    if pi_info:
        try:
            existing = stripe.PaymentIntent.retrieve(pi_info['id'])
            if (existing and existing.status in reusable_statuses
                    and existing.amount == amount_pennies
                    and existing.currency == currency):
                intent = existing
        except InvalidRequestError:
            intent = None  # fall to create new

    if intent is None:
        intent = stripe.PaymentIntent.create(amount=amount_pennies, currency=currency)

    session['stripe_pi'] = {'id': intent.id, 'amount': intent.amount}
    session.modified = True
    return intent

@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'GET':
        if 'bag' in request.session:
            request.session['checkout'] = request.session['bag']
            request.session.modified = True
        else:
            messages.error(request, "There's nothing in your bag to check out.")
            return redirect(reverse('items'))

        checkout_data = request.session.get('checkout', {})
        if not checkout_data:
            messages.error(request, "There's nothing in your checkout at the moment.")
            return redirect(reverse('items'))

        current_checkout = checkout_context(request)
        checkout_items = current_checkout.get('checkout_items', [])
        checkout_total = current_checkout.get('checkout_total', Decimal('0.00'))
        deposit_total = current_checkout.get('deposit_total', Decimal('0.00'))
        site_fee = (checkout_total * Decimal('0.10')).quantize(Decimal("0.01"))
        delivery = Decimal('0.00')
        grand_total = (checkout_total + deposit_total + site_fee + delivery).quantize(Decimal("0.01"))
        stripe_total = int(grand_total * 100)

        if stripe_total < 30:
            messages.error(request, "Total must be at least £0.30 to proceed with payment.")
            return redirect(reverse('reservation:view_bag'))

        intent = _get_or_create_payment_intent(
            stripe_secret_key=stripe_secret_key,
            amount_pennies=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            session=request.session,
        )

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'postcode': profile.postal_code,
                    'town_or_city': profile.city,
                    'street_address1': profile.house_number,
                    'street_address2': profile.street_name,
                    'country': '',
                    'county': '',
                })
            except Profile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'checkout_items': checkout_items,
            'checkout': checkout_data,
            'checkout_total': checkout_total,
            'deposit_total': deposit_total,
            'site_fee': site_fee,
            'checkout_grand_total': grand_total,
            'checkout_product_count': current_checkout.get('checkout_product_count', 0),
            'delivery': delivery,
        }

        return render(request, 'checkout/checkout.html', context)

    # Submit order
    if request.method == 'POST':
        checkout_data = request.session.get('checkout', {})

        if not checkout_data:
            messages.error(request, "There's nothing to check out.")
            return redirect(reverse('items'))

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
            'notes': request.POST.get('notes', ''),
            'delivery_cost': request.POST.get('delivery_cost') or 0,
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            # Stripe PI linkage
            client_secret = request.POST.get('client_secret', '')
            pid = client_secret.split('_secret')[0] if client_secret else ''
            if not pid:
                pid = request.session.get('stripe_pi', {}).get('id', '')
            order.stripe_pid = pid
            order.original_checkout = json.dumps(checkout_data)

            # Totals
            current = checkout_context(request)
            checkout_total = current.get('checkout_total', Decimal('0.00'))
            deposit_total = current.get('deposit_total', Decimal('0.00'))
            site_fee = (checkout_total * Decimal('0.10')).quantize(Decimal('0.01'))

            try:
                delivery_cost = Decimal(str(form_data.get('delivery_cost') or 0)).quantize(Decimal('0.01'))
            except Exception:
                delivery_cost = Decimal('0.00')

            grand_total = (checkout_total + deposit_total + site_fee + delivery_cost).quantize(Decimal('0.01'))

            order.order_total = checkout_total
            order.deposit_total = deposit_total
            order.site_fee = site_fee
            order.delivery_cost = delivery_cost
            order.grand_total = grand_total
            order.save()

            # Create order line items
            for item_id, item_data in checkout_data.items():
                try:
                    product = Product.objects.get(id=item_id)
                    raw_start = item_data.get('start_date')
                    raw_end = item_data.get('end_date')
                    duration = int(item_data.get('duration', 1))

                    if not raw_start or not raw_end:
                        messages.error(request, f"Rental dates for {product.name} are required.")
                        order.delete()
                        return redirect(reverse('checkout'))

                    try:
                        start_date = datetime.strptime(raw_start, DATE_FMT).date()
                        end_date = datetime.strptime(raw_end, DATE_FMT).date()
                    except ValueError:
                        messages.error(request, f"Invalid date format for {product.name}. Use DD/MM/YYYY.")
                        order.delete()
                        return redirect(reverse('checkout'))

                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        start_date=start_date,
                        end_date=end_date,
                        rental_duration=duration,
                    )
                except Product.DoesNotExist:
                    messages.error(request, "A product in your checkout wasn't found. Please try again.")
                    order.delete()
                    return redirect(reverse('checkout'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
            return redirect(reverse('checkout'))

@login_required
def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Clear old bag
    request.session.pop('bag', None)

    # Attach order to profile if logged in
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            order.user_profile = profile
            order.save()

            if save_info:
                profile_data = {
                    'phone_number': order.phone_number,
                    'postal_code': order.postcode,
                    'city': order.town_or_city,
                    'house_number': order.street_address1,
                    'street_name': order.street_address2,
                }
                user_profile_form = ProfileForm(profile_data, instance=profile)
                if user_profile_form.is_valid():
                    user_profile_form.save()
        except Profile.DoesNotExist:
            pass

    # Email renter confirmation
    renter_subject = render_to_string(
        "checkout/confirmation_emails/confirmation_email_subject.txt",
        {"order": order}
    ).strip()

    renter_body = render_to_string(
        "checkout/confirmation_emails/confirmation_email_body.txt",
        {"order": order, "contact_email": settings.DEFAULT_FROM_EMAIL}
    )

    send_mail(
        renter_subject,
        renter_body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

    # Email item owner
    for lineitem in order.lineitems.all():
        owner = lineitem.product.user
        if owner and owner.email:
            owner_subject = render_to_string(
                "checkout/confirmation_emails/owner_confirmation_email_subject.txt",
                {"order": order, "product": lineitem.product}
            ).strip()

            owner_body = render_to_string(
                "checkout/confirmation_emails/owner_confirmation_email_body.txt",
                {"order": order, "product": lineitem.product, "renter": order.full_name}
            )

            send_mail(
                owner_subject,
                owner_body,
                settings.DEFAULT_FROM_EMAIL,
                [owner.email],
                fail_silently=False,
            )

    # Success message
    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. '
        f'A confirmation email has been sent to {order.email}.'
    )

    # Cleanup session
    request.session.pop('checkout', None)
    request.session.pop('stripe_pi', None)
    request.session.modified = True

    return render(request, "checkout/checkout_success.html", {"order": order})
