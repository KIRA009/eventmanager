from utils.decorators import validate
from utils.validator_helpers import make_string_object, make_number_object, make_array_object, make_email_object


register_view_schema = validate(
    make_number_object("college"),
    make_string_object("name"),
    make_email_object("email"),
    make_string_object("password"),
    make_string_object("phone", False),
    make_string_object("username"),
)


login_view_schema = validate(
    make_string_object("username"),
    make_string_object("password")
)

send_verification_schema = validate(
    make_email_object("email")
)

get_user_schema = validate(
    make_string_object("username")
)

del_link_schema = validate(
    make_number_object("id")
)

update_link_sequence_schema = validate(
    make_array_object('links', 'number')
)

update_user_schema = validate(
    make_string_object("name"),
    make_string_object("username"),
    make_email_object("email")
)