from backend.database.core import db
from backend.database import User, UserRole
from backend.auth import user_manager

user = User(
    email="test@example.com",
    password=user_manager.hash_password("password"),
    role=UserRole.PUBLIC,
    first_name="Test",
    last_name="Example",
)

user_exists = (
    db.session.query(User).filter_by(email=user.email).first() is not None
)

if not user_exists:
    user.create()
