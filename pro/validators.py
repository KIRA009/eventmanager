from utils.decorators import validate
from utils.validator_helpers import make_string_object


get_user_schema = validate(
    make_string_object("username")
)