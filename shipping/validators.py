from utils.decorators import validate
from utils.validator_helpers import make_number_object, make_string_object, make_dict_object, make_email_object


get_shipping_expense_schema = validate(
	make_number_object("weight"),
	make_string_object("order_id")
)

create_shipping_schema = validate(
	make_number_object("courier_id"),
	make_string_object("order_id"),
	make_number_object("length"),
	make_number_object("breadth"),
	make_number_object("height"),
	make_number_object("weight"),
)