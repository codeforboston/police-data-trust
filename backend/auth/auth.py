from ..database import db, User
from flask_user import SQLAlchemyAdapter
from flask_user import UserManager
from datetime import timezone, datetime
from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
)
from flask import current_app

user_manager = UserManager(SQLAlchemyAdapter(db, User))


def refresh_token(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = now + current_app.config["TOKEN_EXPIRATION"]

        if target_timestamp.timestamp() > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
