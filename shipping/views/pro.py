from django.views import View

from shipping.validators import *
from shipping.utils import get_shipment_expense, create_shipment
from shipping.models import Shipment


class GetShipmentExpenseView(View):
	@get_shipping_expense_schema
	def post(self, request):
		return get_shipment_expense(request.json)


class CreateShippingView(View):
	@create_shipping_schema
	def post(self, request):
		data = request.json
		shipment = create_shipment(data)
		return dict(shipment=shipment.detail())
