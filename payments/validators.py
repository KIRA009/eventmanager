from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_number_object

update_order_schema = validate(
    make_string_object("status"),
    make_number_object("item_id")
)

refund_order_schema = validate(
    make_string_object("order_id")
)