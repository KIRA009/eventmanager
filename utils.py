from django.http import JsonResponse


def jsonify(data):
    status_code = int(data.get("status_code", 200))
    if "status_code" in data:
        del data["status_code"]
    return JsonResponse(data, status=status_code)


def is_admin(func):
    def inner(*args, **kwargs):
        request = args[0]
        print(request.user.is_superuser)
        return func(*args, **kwargs)

    return inner
