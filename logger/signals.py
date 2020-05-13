from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from django.utils.timezone import localdate, now, timedelta
from time import mktime

from event_app.models import User
from payments.models import Order
from .utils import send_email_to_admins
from event_manager.settings import DEBUG
from payments.models import Subscription
from payments.utils import update_subscription


@receiver(post_save, sender=User)
@receiver(post_save, sender=Order)
def send_email(sender, **kwargs):
    if DEBUG:
        return
    sender = sender.__name__
    instance = kwargs['instance']
    _vars = {}
    if sender == 'User':
        if not kwargs['created']:
            return
        _vars['model_name'] = 'New user registered'
        _vars['message'] = f'{instance.email} registered with {instance.phone if instance.phone else "no phone number"}'
        sub = Subscription(sub_id=str(uuid4()), sub_type=Subscription.PROPACK, user=instance)
        update_subscription(sub, start_date=int(mktime(localdate(now()).timetuple())),
                            end_date=int(mktime((localdate(now()) + timedelta(days=365)).timetuple())))
    elif sender == 'Order':
        if not instance.paid:
            return
        _vars['model_name'] = 'New order receieved and paid'
        _vars['message'] = f'{instance.user.email if instance.user.email else instance.meta_data["user_details"]["email"]} paid {instance.amount} for {instance.meta_data}'
    send_email_to_admins('new_object', _vars['model_name'], **_vars)
