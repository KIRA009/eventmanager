from .middleware import jsonify
from .exceptions import AccessDenied


def decorator(func, test_func):
    def inner(*args, **kwargs):
        request = args[0]
        if 'User' in request.__dict__:
            if test_func(request.User):
                return func(*args, **kwargs)
        elif request.user.is_authenticated:
            if test_func(request.user):
                return func(*args, **kwargs)
        raise AccessDenied()

    return inner


def login_required(func):
    return decorator(func, lambda u: u.is_authenticated)
