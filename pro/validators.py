from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_array_object, make_number_object,\
    make_number_or_string_object


get_user_schema = validate(
    make_string_object("username")
)

create_product_schema = validate(
    make_string_object("name"),
    make_string_object("description"),
    make_number_or_string_object("disc_price"),
    make_number_or_string_object("price"),
)
