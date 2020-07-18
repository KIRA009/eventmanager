from utils.validator_helpers import make_number_object, make_string_object
from utils.decorators import validate

read_notification_schema = validate(
	make_number_object("notif_id")
)

update_token_schema = validate(
	make_string_object("token")
)
