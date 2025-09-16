from decimal import Decimal
from datetime import datetime, date, timedelta
import json

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order, OrderLineItem
from items.models import Product
from profiles.models import Profile


DATE_FMT = "%d/%m/%Y"  # Match frontend format
FEE_RATE = Decimal("0.10")


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    # Helpers

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            "checkout/confirmation_emails/confirmation_email_subject.txt",
            {"order": order},
        ).strip()
        body = render_to_string(
            "checkout/confirmation_emails/confirmation_email_body.txt",
            {"order": order, "contact_email": settings.DEFAULT_FROM_EMAIL},
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email],
            fail_silently=True,
        )

    def _parse_checkout_totals(self, checkout_dict):
        """
        Recompute deposit_total and site_fee from the checkout snapshot.
        """
        rental_total = Decimal("0.00")
        deposit_total = Decimal("0.00")

        for item_id, item_data in checkout_dict.items():
            try:
                product = Product.objects.get(pk=item_id)
            except Product.DoesNotExist:
                continue

            # Parse duration
            duration = item_data.get("duration")
            try:
                duration = int(duration) if duration is not None else None
            except (TypeError, ValueError):
                duration = None

            if duration is None:
                try:
                    start = datetime.strptime(
                        item_data.get("start_date"), DATE_FMT
                    ).date()
                    end = datetime.strptime(
                        item_data.get("end_date"), DATE_FMT
                    ).date()
                    duration = max((end - start).days, 1)
                except Exception:
                    duration = 1

            price = Decimal(str(getattr(product, "price", 0) or 0))
            deposit = Decimal(str(getattr(product, "deposit", 0) or 0))

            rental_total += price * Decimal(duration)
            deposit_total += deposit

        site_fee = (rental_total * FEE_RATE).quantize(Decimal("0.01"))
        return (
            rental_total.quantize(Decimal("0.01")),
            deposit_total.quantize(Decimal("0.01")),
            site_fee,
        )

    def _create_order_from_metadata(
        self, intent, checkout_dict, profile
    ):
        """
        Create an Order + OrderLineItems
        """
        billing_details = (
            intent.charges.data[0].billing_details
            if intent.charges and intent.charges.data
            else {}
        )
        shipping_details = getattr(intent, "shipping", None)

        # Clean shipping address
        if shipping_details and getattr(
            shipping_details, "address", None
        ):
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

        rental_total, deposit_total, site_fee = (
            self._parse_checkout_totals(checkout_dict)
        )

        order = Order.objects.create(
            user_profile=profile,
            full_name=(
                shipping_details.name if shipping_details else ""
            ),
            email=(
                billing_details.email if billing_details else ""
            ),
            phone_number=(
                shipping_details.phone if shipping_details else ""
            ),
            country=(
                shipping_details.address.country
                if shipping_details and shipping_details.address
                else ""
            ),
            postcode=(
                shipping_details.address.postal_code
                if shipping_details and shipping_details.address
                else ""
            ),
            town_or_city=(
                shipping_details.address.city
                if shipping_details and shipping_details.address
                else ""
            ),
            street_address1=(
                shipping_details.address.line1
                if shipping_details and shipping_details.address
                else ""
            ),
            street_address2=(
                shipping_details.address.line2
                if shipping_details and shipping_details.address
                else ""
            ),
            county=(
                shipping_details.address.state
                if shipping_details and shipping_details.address
                else ""
            ),
            delivery_cost=Decimal("0.00"),
            deposit_total=deposit_total,
            site_fee=site_fee,
            order_total=rental_total,
            grand_total=rental_total + deposit_total + site_fee,
            original_checkout=json.dumps(checkout_dict),
            stripe_pid=intent.id,
        )

        # Create line items
        for item_id, item_data in checkout_dict.items():
            try:
                product = Product.objects.get(pk=item_id)
            except Product.DoesNotExist:
                continue

            # Parse dates/duration
            start = item_data.get("start_date")
            end = item_data.get("end_date")
            dur = item_data.get("duration")

            try:
                start_date = (
                    datetime.strptime(start, DATE_FMT).date()
                    if start
                    else None
                )
                end_date = (
                    datetime.strptime(end, DATE_FMT).date()
                    if end
                    else None
                )
            except Exception:
                start_date, end_date = None, None

            try:
                duration = int(dur) if dur is not None else None
            except (TypeError, ValueError):
                duration = None

            if not duration and start_date and end_date:
                duration = max((end_date - start_date).days, 1)
            if not duration:
                duration = 1

            # Fallback for missing dates
            if not start_date or not end_date:
                start_date = date.today()
                end_date = start_date + timedelta(days=duration)

            OrderLineItem.objects.create(
                order=order,
                product=product,
                start_date=start_date,
                end_date=end_date,
                rental_duration=duration,
            )

        # Ensure totals are correct
        return order

    # Handlers

    def handle_event(self, event):
        """Unknown event handlers"""
        return HttpResponse(
            content=f'Unhandled event: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Mark the order paid when Stripe confirms the PaymentIntent.
        """
        intent = event.data.object
        pid = intent.id
        metadata = getattr(intent, "metadata", {}) or {}

        # Attach to the existing order by stripe_pid
        order = (
            Order.objects.filter(stripe_pid=pid)
            .order_by("-date")
            .first()
        )
        if order:
            # Confirmed to reflect payment status
            try:
                order.order_status = "confirmed"
                order.save(update_fields=["order_status"])
            except Exception:
                pass

            # Update profile info if requested
            self._maybe_save_profile(intent)
            self._send_confirmation_email(order)
            return HttpResponse(
                content="Webhook: updated existing order",
                status=200,
            )

        # Order from metadata
        try:
            checkout_json = metadata.get("checkout", "{}")
            checkout_dict = json.loads(checkout_json)
        except Exception:
            checkout_dict = {}

        profile = self._maybe_save_profile(intent)
        try:
            order = self._create_order_from_metadata(
                intent, checkout_dict, profile
            )
        except Exception as e:
            return HttpResponse(
                content=f"Webhook error creating order: {e}",
                status=500,
            )

        self._send_confirmation_email(order)
        return HttpResponse(
            content="Webhook: created order from metadata",
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Payment failed: {event["type"]}',
            status=200,
        )

    # Profile helpers

    def _maybe_save_profile(self, intent):
        """
        If metadata.save_info is truthy and a username exists,
        update the profile defaults using the shipping details.
        """
        metadata = getattr(intent, "metadata", {}) or {}
        username = metadata.get("username")
        save_info = metadata.get("save_info")

        if not username or username in (
            "AnonymousUser", "anon", "None"
        ):
            return None

        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return None

        if save_info:
            shipping = getattr(intent, "shipping", None)
            if shipping and getattr(shipping, "address", None):
                profile.phone_number = (
                    shipping.phone or profile.phone_number
                )
                profile.country = (
                    shipping.address.country or profile.country
                )
                profile.postal_code = (
                    shipping.address.postal_code or profile.postal_code
                )
                profile.city = (
                    shipping.address.city or profile.city
                )
                profile.house_number = (
                    shipping.address.line1 or profile.house_number
                )
                profile.street_name = (
                    shipping.address.line2 or profile.street_name
                )
                profile.save()

        return profile
