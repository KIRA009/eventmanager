from django.http import JsonResponse
import jwt
from django.db import models
from django.utils import timezone as tz
import django.middleware.common as common
import json
from django.contrib.auth import get_user_model
from django.core import serializers
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from event_manager.settings import (
    SECRET_KEY,
    SENDGRIDAPIKEY,
    EMAIL_FROM
)


def send_email(emails, subject, message):
    message = Mail(
        from_email=EMAIL_FROM, to_emails=emails, subject=subject, html_content=message
    )
    sg = SendGridAPIClient(SENDGRIDAPIKEY)
    sg.send(message)


def jsonify(data):
    status_code = int(data.get("status_code", 200))
    if "status_code" in data:
        del data["status_code"]
    return JsonResponse(data, status=status_code)


def retrieve_token(token):
    try:
        return True, jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return False, str(e)


def create_token(**kwargs):
    return jwt.encode(kwargs, SECRET_KEY, algorithm="HS256").decode()


class CustomMiddleware(common.CommonMiddleware):
    def process_request(self, request):
        super(CustomMiddleware, self).process_request(request)
        if request.method == "OPTIONS" or "/admin/" in request.path:
            return
        token = request.headers.get("Token")
        if token is not None:
            decoded, token = retrieve_token(token)
            if decoded:
                for i in ["username", "len_email"]:
                    if token.get(i) is None:
                        return dict(error="Invalid token", status_code=401)
                username = token["username"][: token["len_email"]]
                password = token["username"][3 + token["len_email"]:]
                model = get_user_model()
                try:
                    user = model.objects.get(email=username, password=password)
                    if user:
                        # if not user.is_validated:
                        # return dict(error="Email not verified", status_code=401)
                        # if user.last_login.isoformat() == token["login_time"]:
                        request.User = user
                except model.DoesNotExist:
                    pass
        if request.content_type == "application/json":
            request.json = json.loads(request.body)

    def process_response(self, request, response):
        if "/admin/" in request.path:
            return super().process_response(request, response)
        if isinstance(response, dict):
            response = jsonify(response)
        return super().process_response(request, response)


class BaseManager(models.Manager):
    def get(self, **kwargs):
        try:
            return super(BaseManager, self).get(**kwargs)
        except self.model.DoesNotExist:
            return None


class AutoCreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = tz.now()
            self.updated_at = self.created_at
        else:
            auto_updated_at_is_disabled = kwargs.pop("disable_auto_updated_at", False)
            if not auto_updated_at_is_disabled:
                self.updated_at = tz.now()
        super(AutoCreatedUpdatedMixin, self).save(*args, **kwargs)

    def detail(self):
        ret = json.loads(serializers.serialize('json', [self]))[0]
        ret['fields']['id'] = ret['pk']
        del ret['fields']['created_at']
        del ret['fields']['updated_at']
        return ret['fields']


def decorator(func, test_func):
    def inner(*args, **kwargs):
        request = args[0]
        if 'User' in request.__dict__:
            if test_func(request.User):
                return func(*args, **kwargs)
        elif request.user.is_authenticated:
            if test_func(request.user):
                return func(*args, **kwargs)
        return jsonify(dict(error="Access denied", status_code=401))

    return inner


def login_required(func):
    return decorator(func, lambda u: u.is_authenticated)
