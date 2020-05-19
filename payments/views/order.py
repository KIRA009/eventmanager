from django.views import View
from django.shortcuts import redirect
from collections import namedtuple
import uuid

from payments.models import Order, OrderItem
from event_app.models import User
from pro.models import Product
from payments.utils import create_order, create_order_form
from payments.validators import update_order_schema
from utils.exceptions import AccessDenied
from event_manager.settings import PAYMENT_CANCEL_URL, PAYMENT_CALLBACK_URL


class OrderView(View):
    def get(self, request):
        return dict(orders=request.User.orders.all().detail())

    # @create_order_schema
    def post(self, request):
        data = request.json
        amount = 0
        shipping_charges = 0
        items = []
        for item in data["items"]:
            if item["type"] == "product":
                prod = Product.objects.get(id=item["id"])
                if prod.stock < int(item['meta_data']['quantity']):
                    raise AccessDenied(f'{prod.name} has less stock than requested')
                items.append((prod, item['meta_data']))
                amount += prod.disc_price
                shipping_charges = max(shipping_charges, prod.shipping_charges)
        if amount == 0:
            raise AccessDenied("Total amount is 0")
        amount += shipping_charges
        user_details = data['user_details']
        _User = namedtuple('_User', ['email'])
        user = User.objects.filter(email=user_details['email']).first()
        if not user:
            user = _User(email=user_details['email'])
        if data['cod']:
            order_id = str(uuid.uuid4())
        else:
            order_id = create_order(amount)
        order = Order.objects.create(
            order_id=order_id, amount=amount, user=user if not isinstance(user, _User) else None,
            meta_data=dict(user_details=user_details), cod=data['cod'],
            shipping_charges=shipping_charges
        )
        items = [OrderItem(order=item[0], order_id=order, index=i, meta_data=item[1])
                 for i, item in enumerate(items)]
        OrderItem.objects.bulk_create(items)
        if order.cod:
            return dict(message="Order received")
        return dict(form=create_order_form(order_id, user))


class UpdateSoldProductsView(View):
    @update_order_schema
    def post(self, request):
        data = request.json
        item = Order.objects.get(id=data['item_id'])
        if item.items.first().order.user != request.User:
            raise AccessDenied()
        item.status = data['status']
        item.save()
        return dict(item=item.detail())


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
