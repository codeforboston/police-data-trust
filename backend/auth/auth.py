from ..database import db, User
from flask_user import SQLAlchemyAdapter
from flask_user import UserManager

user_manager = UserManager(SQLAlchemyAdapter(db, User))

