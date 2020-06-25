import requests
from django.utils.timezone import datetime

from event_manager.settings import SHIPPING_TOKEN, DEBUG
from utils.exceptions import AccessDenied
from payments.models import Order
from shipping.models import Shipment


BASE_URL = "https://apiv2.shiprocket.in/v1/external"

headers = {
	'Authorization': f'Bearer {SHIPPING_TOKEN}'
}


def get_shipment_expense(data, user):
	order = Order.objects.get(order_id=data['order_id'], seller__user=user)
	del data['order_id']
	data['pickup_postcode'] = order.seller.pincode
	data.update(**dict(
		cod=order.cod,
		delivery_postcode=order.meta_data['user_details']['pincode']
	))
	res = requests.get(
		f'{BASE_URL}/courier/serviceability/',
		json=data,
		headers=headers
	).json()
	if res['status'] != 200:
		if 'message' in res:
			raise AccessDenied(res['message'])
		raise AccessDenied('Some error happened')
	return dict(
		recommended_courier_id=res['data']['shiprocket_recommended_courier_id'],
		couriers=res['data']['available_courier_companies']
	)


def create_shipment(data, user):
	expense = get_shipment_expense(dict(
		order_id=data['order_id'],
		weight=data['weight']
	), user)
	rate = list(
		filter(lambda x: x['courier_company_id'] == expense['recommended_courier_id'], expense['couriers'])
	)[0]['rate']
	# return Shipment.objects.first()
	order = Order.objects.select_related('seller', 'seller__user').get(order_id=data['order_id'], seller__user=user)
	if order.status != Order.PROCESSED:
		raise AccessDenied("Order has already been upgraded from processing")
	user_details = order.meta_data['user_details']
	seller = order.seller
	json = {
		"request_pickup": not DEBUG,
		"courier_id": data['courier_id'],
		"order_id": 'a' + order.order_id[:19],
		"order_date": order.created_at.date().isoformat(),
		"channel_id": 657510,
		"billing_customer_name": user_details['name'].split()[0],
		"billing_last_name": ' '.join(user_details['name'].split()[1:]),
		"billing_address": user_details['address'],
		"billing_city": user_details['city'],
		"billing_pincode": user_details['pincode'],
		"billing_state": user_details['state'],
		"billing_country": user_details['country'],
		"billing_email": user_details['email'],
		"billing_phone": user_details['number'],
		"shipping_is_billing": True,
		"order_items": [
			dict(
				name=item.order.name,
				sku=item.order.name,
				units=item.meta_data['quantity'],
				selling_price=item.order.price
			) for item in order.items.all()
		],
		"payment_method": "COD" if order.cod else "Prepaid",
		"shipping_charges": order.shipping_charges,
		"total_discount": sum((item.order.price - item.order.disc_price) for item in order.items.all()),
		"sub_total": order.amount - order.shipping_charges,
		"length": data['length'],
		"breadth": data['length'],
		"height": data['length'],
		"weight": data['weight'],
		"pickup_location": seller.pickup_location,
		"vendor_details": dict(
			email=seller.user.email,
			phone=seller.user.phone,
			name=seller.user.name,
			address=seller.shop_address,
			city=seller.city,
			state=seller.state,
			country=seller.country,
			pin_code=seller.pincode,
			pickup_location=seller.pickup_location
		)
	}
	res = requests.post(
		f'{BASE_URL}/shipments/create/forward-shipment',
		json=json,
		headers=headers
	).json()
	payload = res['payload']
	order.update_status(Order.CONFIRMED)
	order.seller.amount -= rate
	order.seller.save()
	return Shipment.objects.create(
		courier_company_id=payload['courier_company_id'],
		courier_name=payload['courier_name'],
		awb_code=payload['awb_code'],
		shipment_id=payload['shipment_id'] if not DEBUG else 'dummy shipment id',
		shipment_order_id=payload['order_id'],
		label_url=payload['label_url'],
		manifest_url=payload['manifest_url'] if not DEBUG else 'http://example.com',
		pickup_token_number=payload['pickup_token_number'] if not DEBUG else 'dummy value',
		routing_code=payload['routing_code'],
		applied_weight=payload['applied_weight'],
		pickup_scheduled_date=datetime.strptime(
			payload['pickup_scheduled_date'], '%Y-%m-%dT%H:%M:%S'
		) if not DEBUG else order.created_at,
		order=order
	)
