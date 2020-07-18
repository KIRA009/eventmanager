from .models import Notification


def create_notification(
		user, header="Test notification", description="Test description for test notification", meta_data=None
):
	from utils.tasks import send_push_message
	if meta_data is None:
		meta_data = dict()
	notif = Notification.objects.create(
		user=user,
		header=header,
		description=description,
		meta_data=meta_data
	)
	send_push_message([
		dict(
			token=user.notif_token, description=notif.description, title=notif.header, id=notif.id,
			unread_notifs=user.notifications.filter(read_at=None).count()
		)
	])
