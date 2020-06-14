from .models import Notification


def create_notification(
		user, header="Test notification", description="Test description for test notification", meta_data=None
):
	if meta_data is None:
		meta_data = dict()
	Notification.objects.create(
		user=user,
		header=header,
		description=description,
		meta_data=meta_data
	)
