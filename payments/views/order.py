from django.views import View
from django.shortcuts import redirect
from collections import namedtuple
import uuid

from payments.models import Order, OrderItem
from event_app.models import User
from pro.models import Product
from payments.utils import create_order_form, create_order


class OrderView(View):
    def get(self, request):
        return dict(orders=request.User.orders.all().detail())

    # @create_order_schema
    def post(self, request):
        data = request.json
        amount = 0
        items = []
        for item in data['items']:
            if item['type'] == 'product':
                product = Product.objects.get(id=item['id'])
                items.append(product)
                amount += int(item['meta_data']['quantity']) * product.disc_price
        user_details = data['user_details']
        _User = namedtuple('_User', ['name', 'email', 'phone'])
        user = User.objects.filter(email=user_details['email']).first()
        if not user:
            user = User.objects.filter(phone=user_details['phone']).first()
        if not user:
            user = _User(name=user_details['name'], phone=user_details['phone'], email=user_details['email'])
        if data['cod']:
            order_id = str(uuid.uuid4())
        else:
            order_id = create_order(amount)
        order = Order.objects.create(
            order_id=order_id, amount=amount, user=user if not isinstance(user, _User) else None,
            meta_data=dict(user_details=user_details), cod=data['cod']
        )
        items = [OrderItem(order=item, order_id=order, index=i, meta_data=data['items'][i])
                 for i, item in enumerate(items)]
        OrderItem.objects.bulk_create(items)
        if order.cod:
            return dict(message="Order received")
        return dict(
            form=create_order_form(order_id, data, user)
        )


class OrderCallBackView(View):
    def post(self, request):
        scheme = request.META["wsgi.url_scheme"]
        server = request.META["HTTP_HOST"]
        data = request.POST.dict()
        if 'razorpay_order_id' not in data:
            return redirect(f"{scheme}://{server}")
        username = Order.objects.get(order_id=data['razorpay_order_id']).items.first().order.user.username
        return redirect(f"{scheme}://{server}/{username}/payment/success")


class OrderCancelView(View):
    def post(self, request):
        scheme = request.META["wsgi.url_scheme"]
        server = request.META["HTTP_HOST"]
        return redirect(f"{scheme}://{server}")
