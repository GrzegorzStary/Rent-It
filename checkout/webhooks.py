from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWH_Handler
import stripe


@csrf_exempt
@require_POST
def webhook(request):
    """
    Listen for webhooks from Stripe and dispatch to the appropriate handler.
    """
    wh_secret = getattr(settings, "STRIPE_WH_SECRET", None)
    stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    if not sig_header or not wh_secret:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=str(e), status=400)

    handler = StripeWH_Handler(request)

    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_intent_payment_failed,
    }

    event_type = event.get("type")
    event_handler = event_map.get(event_type, handler.handle_event)
    return event_handler(event)
