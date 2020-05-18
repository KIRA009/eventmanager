from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import stripe
import json

from payments.models import Order, Seller
from payments.utils import get_payment_intent
from event_manager.settings import STRIPE_KEY, STRIPE_WEBHOOK_SECRET
from utils.exceptions import NotFound
from utils.tasks import create_invoice


webhook_secret = STRIPE_WEBHOOK_SECRET
stripe.api_key = STRIPE_KEY


@method_decorator(csrf_exempt, name="dispatch")
class PaymentWebhookView(View):
    def post(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError as e:
            return dict()
        except stripe.error.SignatureVerificationError as e:
            return dict()
        if event.type == "checkout.session.completed":
            session = event.data.object
            try:
                order = Order.objects.get(order_id=session.id)
                order.paid = True
                intent = get_payment_intent(session.payment_intent)
                charge = intent.charges.data[0]
                order.meta_data['payment'] = dict(
                    id=intent.id,
                    method=json.loads(json.dumps(charge.payment_method_details)),
                    receipt=charge.receipt_url
                )
                order.save()
                seller = Seller.objects.get_or_create(user=order.items.first().order.user)[0]
                for item in order.items.all():
                    seller.amount += max(0, int(0.97 * item.order.disc_price) - 5)
                    item.order.stock -= int(item.meta_data['quantity'])
                    item.order.save()
                seller.save()
                create_invoice(order.id, seller.id)
            except NotFound:
                pass
        return dict()
