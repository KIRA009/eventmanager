import django.middleware.common as common
from utils import jsonify
import json
from django.contrib.auth import get_user_model
from django.utils import timezone as tz

from .urls import unauth_urls, auth_urls
from utils import retrieve_token


class CustomMiddleware(common.CommonMiddleware):
    def process_request(self, request):
        is_auth_request = False
        for url in auth_urls:
            if url.pattern.regex.search(request.path_info[1:]):
                is_auth_request = True
                break
        super(CustomMiddleware, self).process_request(request)
        if request.method == "OPTIONS" or request.path.startswith("/admin/"):
            return
        request.is_auth_request = is_auth_request
        if is_auth_request:
            token = request.headers.get("Token")
            if token is None:
                return dict(error="No token found", status_code=401)
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
                    if user.last_login.isoformat() == token["login_time"]:
                        request.user = user
                    else:
                        return dict(
                            error="Token corrupted, please log in again",
                            status_code=401,
                        )
                except model.DoesNotExist:
                    return dict(error="Invalid token", status_code=401)
            else:
                return dict(error=token, status_code=401)
        if request.body.decode():
            request.json = json.loads(request.body)

    def process_response(self, request, response):
        if request.path.startswith("/admin/"):
            return super().process_response(request, response)
        if isinstance(response, dict):
            response = jsonify(response)
        return super().process_response(request, response)
