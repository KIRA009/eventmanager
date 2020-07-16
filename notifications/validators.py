from utils.validator_helpers import make_number_object
from utils.decorators import validate

read_notification_schema = validate(
		make_number_object("notif_id")
)