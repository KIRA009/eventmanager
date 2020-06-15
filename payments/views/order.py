from django.views import View
from django.shortcuts import redirect

from payments.models import Order, Seller
from payments.utils import create_order_form, create_order
from payments.validators import *
from utils.exceptions import AccessDenied, NotFound
from event_manager.settings import PAYMENT_CANCEL_URL, PAYMENT_CALLBACK_URL
from utils.tasks import handle_order, refund_order


class OrderView(View):
    def get(self, request):
        return dict(orders=request.User.orders.all().detail())

    # @create_order_schema
    def post(self, request):
        data = request.json
        user_details = data['user_details']
        seller = Seller.objects.get(user__username=data['seller'])
        order_id, user = create_order(data['cod_items'], 'cod', user_details, seller)
        handle_order(dict(
                payload=dict(
                    order=dict(
                        entity=dict(id=order_id)
                    ),
                    payment=dict(
                        entity=dict(
                            order_id=order_id
                        )
                    )
                )
            ))
        order_id, user = create_order(data['online_items'], 'online', user_details, seller)
        if order_id:
            return dict(form=create_order_form(order_id, user))
        return dict(message="Order created")


class UpdateSoldProductsView(View):
    @update_order_schema
    def post(self, request):
        data = request.json
        order = Order.objects.get(id=data['item_id'], seller__user=request.User)
        order.update_status(data['status'])
        return dict(item=order.detail())


class GetSoldProductsView(View):
    def get(self, request):
        page_no = int(request.GET.get('pageNo', 1))
        status = str(request.GET.get('delivered', 'true'))
        query = Order.objects.get_sold_products(request.User)
        if status == 'true':
            query = query.filter(status=Order.DELIVERED)
        else:
            query = query.exclude(status=Order.DELIVERED)
        num_pages, page = query.paginate(page_no)
        return dict(orders=page.detail(), num_pages=num_pages)


class OrderCallBackView(View):
    def post(self, request):
        return redirect(PAYMENT_CALLBACK_URL)


class OrderCancelView(View):
    def post(self, request):
        return redirect(PAYMENT_CANCEL_URL)


class OrderRefundView(View):
    @refund_order_schema
    def post(self, request):
        order_id = request.json['order_id']
        order = Order.objects.get(order_id=order_id, seller__user=request.User)
        if order.status in [Order.REFUND_INITIATED, Order.REFUNDED]:
            raise AccessDenied('Refund has already been initiated / processed for this order')
        refund_order(order_id)
        return dict(message="Refund initiated")
