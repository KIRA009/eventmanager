from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_number_object, make_uri_object


get_user_schema = validate(
    make_string_object("username")
)

create_product_schema = validate(
    make_string_object("name"),
    make_string_object("description"),
    make_number_object("disc_price"),
    make_number_object("price"),
    make_string_object("estimated_delivery")
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
    make_string_object("estimated_delivery")
)

delete_product_schema = validate(
    make_number_object("product_id")
)