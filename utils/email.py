from django.core.mail import send_mail

from event_manager.settings import EMAIL_HOST_USER


def send_email(emails, subject, message):
    try:
        send_mail(
            subject=subject,
            message="This is a system generated email",
            from_email=EMAIL_HOST_USER,
            recipient_list=emails,
            html_message=message,
            fail_silently=False
        )
    except Exception as e:
        pass
