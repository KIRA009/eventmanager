import django.middleware.common as common
from utils import jsonify
import json
from django.contrib.auth import get_user_model
from django.utils import timezone as tz

from .urls import unauth_urls, auth_urls
from utils import retrieve_token


class CustomMiddleware(common.CommonMiddleware):
    def process_request(self, request):
        super(CustomMiddleware, self).process_request(request)
        if request.method == "OPTIONS" or "/admin/" in request.path:
            return
        token = request.headers.get("Token")
        if token is not None:
            decoded, token = retrieve_token(token)
            if decoded:
                for i in ["login_time", "username", "len_email"]:
                    if token.get(i) is None:
                        return dict(error="Invalid token", status_code=401)
                username = token["username"][: token["len_email"]]
                password = token["username"][3 + token["len_email"] :]
                model = get_user_model()
                try:
                    user = model.objects.get(email=username, password=password)
                    # if not user.is_validated:
                    # return dict(error="Email not verified", status_code=401)
                    if user.last_login.isoformat() == token["login_time"]:
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
