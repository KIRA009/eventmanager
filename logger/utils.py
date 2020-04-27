from utils import decorator


def admin_required(func):
    return decorator(func, lambda u: u.is_superuser)