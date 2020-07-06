from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_number_object, make_uri_object, make_dict_object, \
    make_boolean_object, make_array_object


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
    make_boolean_object("cod_available"),
    make_boolean_object("opt_for_reselling"),
    make_number_object("resell_margin"),
    make_boolean_object("sizes_available"),
    make_number_object("shipping_charges"),
    make_string_object("category"),
    make_number_object("stock"),
    make_array_object("sizes", _type="object", properties=dict(
        **make_string_object("size"),
        **make_number_object("stock"),
        **make_number_object("resell_margin"),
        **make_number_object("disc_price"),
        **make_number_object("price"),
    ))
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
    make_boolean_object("cod_available"),
    make_boolean_object("online_available"),
    make_boolean_object("opt_for_reselling"),
    make_number_object("resell_margin"),
    make_boolean_object("sizes_available"),
    make_number_object("shipping_charges"),
    make_string_object("category"),
    make_number_object("stock"),
    make_array_object("sizes", _type="object", properties=dict(
        **make_string_object("size"),
        **make_number_object("stock"),
        **make_number_object("resell_margin"),
        **make_number_object("disc_price"),
        **make_number_object("price"),
    ))
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

update_shipping_schema = validate(
    make_string_object("shipping_area"),
    make_string_object("shop_address"),
    make_string_object("city"),
    make_string_object("state"),
    make_string_object("country"),
    make_string_object("pincode"),
    make_boolean_object("is_category_view_enabled")
)

delete_category_schema = validate(
    make_number_object("category_id")
)

update_category_schema = validate(
    make_string_object("category_id"),
    make_string_object("name")
)

search_products_schema = validate(
    make_string_object("query"),
    make_string_object("seller")
)

add_resell_product_schema = validate(
    make_number_object("product_id"),
    make_number_object("resell_margin")
)