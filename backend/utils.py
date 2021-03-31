from functools import wraps
from flask import current_app


def dev_only(func: callable) -> callable:
    """Decorator that ensures a function only runs in the development
    environment. Commands tagged with this will raise an error when you run
    them in production.

    This is mainly used in building CLI commands for dev.
    """

    @wraps(func)
    def _wrap(*args, **kwargs):
        if current_app.env not in ["development", "testing"]:
            raise RuntimeError(
                "You can only run this in the development environment. "
                "Make sure you set up the environment correctly if you "
                "believe you are in dev."
            )
        return func(*args, **kwargs)

    return _wrap
