from utils.decorators import validate
from utils.validator_helpers import make_boolean_object, make_number_object, make_string_object


get_shipping_expense_schema = validate(
	make_number_object("pickup_postcode"),
	make_number_object("delivery_postcode"),
	make_boolean_object("cod"),
	make_number_object("weight")
)

create_shipping_schema = validate(
	make_number_object("courier_id"),
	make_string_object("order_id"),
	make_number_object("length"),
	make_number_object("breadth"),
	make_number_object("height"),
	make_number_object("weight")
)