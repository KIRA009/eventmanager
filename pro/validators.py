from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_number_object, make_uri_object, make_dict_object, \
    make_boolean_object


get_user_schema = validate(
    make_string_object("username")
)

create_product_schema = validate(
    make_string_object("name"),
    make_string_object("description"),
    make_number_object("disc_price"),
    make_number_object("price"),
    make_string_object("estimated_delivery"),
    make_dict_object("meta_data"),
    make_boolean_object("cod_available")
)

add_image_schema = validate(
    make_string_object("product_id")
)

delete_image_schema = validate(
    make_number_object("product_id"),
    make_uri_object("image")
)

update_product_schema = validate(
    make_number_object("id"),
    make_string_object("name"),
    make_string_object("description"),
    make_number_object("disc_price"),
    make_number_object("price"),
    make_string_object("estimated_delivery"),
    make_dict_object("meta_data"),
    make_boolean_object("cod_available")
)

delete_product_schema = validate(
    make_number_object("product_id")
)

update_order_schema = validate(
    make_string_object("status"),
    make_number_object("item_id")
)

retrieve_amount_schema = validate(
    make_number_object("amount")
)

update_bank_details = validate(
    make_string_object("account_holder_name"),
    make_string_object("account_number"),
    make_string_object("ifsc_code")
)