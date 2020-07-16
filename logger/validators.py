from utils.validator_helpers import make_string_object
from utils.decorators import validate

log_client_error_schema = validate(
	make_string_object("username"),
	make_string_object("url"),
	make_string_object("stack_trace")
)
