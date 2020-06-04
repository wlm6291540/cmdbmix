from flask import redirect, url_for, abort, request
from flask_login import current_user
import functools


def auth_required2(endpoint):
    """
    :param endpoint:
    :return:
    判断用户是否有访问endpoint的权限
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.can(endpoint):
                return redirect(url_for('auth.no_permission'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # if not current_user.can(request.endpoint):
        #     return redirect(url_for('auth.no_permission'))
        return func(*args, **kwargs)
    return wrapper
