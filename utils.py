from django.http import JsonResponse
import jwt

from event_manager.settings import SECRET_KEY


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
