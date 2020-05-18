from django.views import View
from django.shortcuts import redirect
from collections import namedtuple
import uuid

from payments.models import Order, OrderItem
from event_app.models import User
from pro.models import Product
from payments.utils import create_order
from payments.validators import update_order_schema
from utils.exceptions import AccessDenied


class OrderView(View):
    def get(self, request):
        return dict(orders=request.User.orders.all().detail())

    # @create_order_schema
    def post(self, request):
        data = request.json
        amount = 0
        order_items = []
        items = []
        for item in data["items"]:
            if item["type"] == "product":
                prod = Product.objects.get(id=item["id"])
                if prod.stock < int(item['meta_data']['quantity']):
                    raise AccessDenied(f'{prod.name} has less stock than requested')
                items.append((prod, item['meta_data']))
                amount += prod.disc_price
                order_items.append(
                    dict(
                        name=prod.name,
                        description=prod.description,
                        images=prod.images,
                        amount=prod.disc_price * 100,
                        currency="inr",
                        quantity=item['meta_data']['quantity'],
                    )
                )
        if amount == 0:
            raise AccessDenied("Total amount is 0")
        user_details = data['user_details']
        _User = namedtuple('_User', ['email'])
        user = User.objects.filter(email=user_details['email']).first()
        if not user:
            user = _User(email=user_details['email'])
        if data['cod']:
            order_id = str(uuid.uuid4())
        else:
            order_id = create_order(order_items, user)
        order = Order.objects.create(
            order_id=order_id, amount=amount, user=user if not isinstance(user, _User) else None,
            meta_data=dict(user_details=user_details), cod=data['cod']
        )
        items = [OrderItem(order=item[0], order_id=order, index=i, meta_data=item[1])
                 for i, item in enumerate(items)]
        OrderItem.objects.bulk_create(items)
        if order.cod:
            return dict(message="Order received")
        return dict(id=order_id)


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
