"""Define the SQL classes for Users."""

from flask import current_app
from argon2 import exceptions as argon2_exceptions
from backend.schemas import JsonSerializable, PropertyEnum
from neomodel import (
    Relationship, StructuredNode,
    StringProperty, DateProperty, BooleanProperty,
    UniqueIdProperty, EmailProperty
)


class UserRole(str, PropertyEnum):
    PUBLIC = "Public"
    PASSPORT = "Passport"
    CONTRIBUTOR = "Contributor"
    ADMIN = "Admin"

    def get_value(self):
        if self == UserRole.PUBLIC:
            return 1
        elif self == UserRole.PASSPORT:
            return 2
        elif self == UserRole.CONTRIBUTOR:
            return 3
        else:
            return 4


# Define the User data-model.
class User(StructuredNode, JsonSerializable):
    __hidden_properties__ = [
        "password_hash", "received_invitations",
        "extended_invitations", "entended_staged_invitations"
    ]
    __property_order__ = [
        "uid", "first_name", "last_name",
        "email", "email_confirmed_at",
        "phone_number", "role", "active"
    ]

    uid = UniqueIdProperty()
    active = BooleanProperty(default=True)

    # User authentication information. The collation="NOCASE" is required
    # to search case insensitively when USER_IFIND_MODE is "nocase_collation".
    email = EmailProperty(required=True, unique_index=True)
    email_confirmed_at = DateProperty()
    password_hash = StringProperty(required=True)

    # User information
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)

    role = StringProperty(
        choices=UserRole.choices(), default=UserRole.PUBLIC.value)

    phone_number = StringProperty()

    # Data Source Relationships
    received_invitations = Relationship(
        'backend.database.models.source.Invitation',
        "RECEIVED")
    extended_invitations = Relationship(
        'backend.database.models.source.Invitation',
        "EXTENDED")
    entended_staged_invitations = Relationship(
        'backend.database.models.source.StagedInvitation',
        "EXTENDED")

    def _get_password_hasher(self):
        """
        Get the password hasher.
        Returns:
            PasswordHasher: The password hasher.
        """
        return current_app.config['PASSWORD_HASHER']

    def verify_password(self, pw: str) -> bool:
        """
        Verify the user's password using bcrypt.
        Args:
            pw (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        try:
            return self._get_password_hasher().verify(self.password_hash, pw)
        except argon2_exceptions.VerifyMismatchError:
            return False
        except argon2_exceptions.VerificationError:
            return False
        except argon2_exceptions.InvalidHash:
            return False

    def set_password(self, pw: str):
        """
        Set the user's password.
        Args:
            pw (str): The password to set.
        """
        self.password_hash = self.hash_password(pw)

    def send_email_verification(self):
        """
        Send an email verification link to the user.
        """
        pass

    def send_password_reset(self):
        """
        Send a password reset link to the user.
        """
        pass

    def send_reset_password_email(self, email: str, reset_token: str):
        """
        Send a password reset link to the user.
        """
        from flask_mail import Message
        from backend.api import mail
        from flask import current_app

        domain = current_app.config["FRONT_END_URL"]
        reset_url = f"{domain}reset?token={reset_token}"

        msg = Message(
            subject='NPDC Password Reset',
            recipients=[email],
            body=(
                f"Hi {email},\n\n"
                "We received a request to reset your password.  "
                "Click the link below to reset it.\n\n"
                "This link will expire in 20 mins.\n\n"
                f"Reset your password: {reset_url}\n\n"
                "If you didn’t request this,"
                "you can safely ignore this email.\n\n"
                "Thanks,\n"
                "NPCD")
                )
        mail.send(msg)

    @property
    def role_enum(self) -> UserRole:
        """
        Get the user's role as an enum.
        Returns:
            UserRole: The user's role as an enum.
        """
        return UserRole(self.role)

    @classmethod
    def hash_password(cls, pw: str) -> str:
        """
        Hash a password.
        Args:
            pw (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return current_app.config['PASSWORD_HASHER'].hash(pw)

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        """
        Get a user by their email address.

        Args:
            email (str): The user's email.

        Returns:
            User: The User instance if found, otherwise None.
        """
        try:
            return cls.nodes.get_or_none(email=email)
        except cls.DoesNotExist:
            return None
