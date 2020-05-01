import django.middleware.common as common
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse

from .token import retrieve_token


def jsonify(data):
    status_code = int(data.get("status_code", 200))
    if "status_code" in data:
        del data["status_code"]
    return JsonResponse(data, status=status_code)


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
