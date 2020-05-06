from utils.decorators import decorator


def pro_required(func):
    return decorator(func, lambda u: u.user_type == "pro")
