from django.db.models.signals import post_save
from django.dispatch import receiver

from event_app.models import User
from payments.models import Order
from .utils import send_email_to_admins


@receiver(post_save, sender=User)
@receiver(post_save, sender=Order)
def send_email(sender, **kwargs):
    sender = sender.__name__
    instance = kwargs['instance']
    _vars = {}
    if sender == 'User':
        if not kwargs['created']:
            return
        _vars['model_name'] = 'New user registered'
        _vars['message'] = f'{instance.email} registered with {instance.phone if instance.phone else "no phone number"}'
    elif sender == 'Order':
        if not instance.paid:
            return
        _vars['model_name'] = 'New order receieved and paid'
        _vars['message'] = f'{instance.user.email} paid {instance.amount} for {instance.meta_data}'
    # send_email_to_admins('new_object', _vars['model_name'], **_vars)
