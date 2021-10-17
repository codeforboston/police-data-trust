from backend.database.core import db
from backend.database import User, UserRole
from backend.auth import user_manager


def create_user(user):
    user_exists = (
        db.session.query(User).filter_by(email=user.email).first() is not None
    )

    if not user_exists:
        user.create()


create_user(
    User(
        email="test@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.PUBLIC,
        first_name="Test",
        last_name="Example",
    )
)

create_user(
    User(
        email="contributor@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.CONTRIBUTOR,
        first_name="Contributor",
        last_name="Example",
    )
)

create_user(
    User(
        email="admin@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.ADMIN,
        first_name="Admin",
        last_name="Example",
    )
)

create_user(
    User(
        email="passport@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.PASSPORT,
        first_name="Passport",
        last_name="Example",
    )
)
