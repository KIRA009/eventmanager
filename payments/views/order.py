from django.views import View
from django.shortcuts import redirect

from payments.models import Order
from payments.utils import create_order_form, create_order
from payments.validators import update_order_schema
from utils.exceptions import AccessDenied
from event_manager.settings import PAYMENT_CANCEL_URL, PAYMENT_CALLBACK_URL


class OrderView(View):
    def get(self, request):
        return dict(orders=request.User.orders.all().detail())

    # @create_order_schema
    def post(self, request):
        data = request.json
        user_details = data['user_details']
        create_order(data['cod_items'], 'cod', user_details)
        order_id, user = create_order(data['online_items'], 'online', user_details)
        if order_id:
            return dict(form=create_order_form(order_id, user))
        return dict(message="Order created")


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
