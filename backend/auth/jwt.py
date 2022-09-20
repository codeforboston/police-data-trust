from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from functools import wraps
from ..database import User
from flask import abort


jwt = JWTManager()


def verify_roles_or_abort(min_role):
    verify_jwt_in_request()
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    if (
        current_user is None
        or current_user.role.get_value() < min_role[0].get_value()
    ):
        abort(403)
        return False
    return True


def blueprint_role_required(*roles):
    def decorator():
        verify_roles_or_abort(roles)

    return decorator


"""
creates a decorator for routes that need verification of a user role

:param roles: roles that are valid for this route to continue
:returns decorator for function
"""


def min_role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if verify_roles_or_abort(roles):
                return fn(*args, **kwargs)

        return decorator

    return wrapper
