from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_number_object, make_array_object, make_dict_object, \
    make_email_object

update_order_schema = validate(
    make_string_object("status"),
    make_number_object("item_id")
)

refund_order_schema = validate(
    make_string_object("order_id"),
    make_string_object("reason")
)


create_order_schema = validate(
    make_array_object("online_items", _type="object", properties=dict(
        **make_string_object("type"),
        **make_number_object("id"),
        **make_dict_object("meta_data", properties=dict(
            **make_number_object("quantity")
        ))
    )),
    make_array_object("cod_items", _type="object", properties=dict(
        **make_string_object("type"),
        **make_number_object("id"),
        **make_dict_object("meta_data", properties=dict(
            **make_number_object("quantity")
        ))
    )),
    make_string_object("seller"),
    make_dict_object("user_details", properties=dict(
        **make_string_object("city"),
        **make_string_object("name"),
        **make_email_object("email"),
        **make_string_object("state"),
        **make_string_object("number"),
        **make_string_object("address"),
        **make_string_object("country"),
        **make_string_object("pincode"),
        **make_string_object("apartment")
    ))
)