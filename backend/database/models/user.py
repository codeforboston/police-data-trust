"""Define the SQL classes for Users."""

import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from backend.schemas import JsonSerializable, PropertyEnum
from neomodel import (
    Relationship, StructuredNode,
    StringProperty, DateProperty, BooleanProperty,
    UniqueIdProperty, EmailProperty
)
from backend.database.models.partner import PartnerMember


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
    __hidden_properties__ = ["password_hash"]
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

    # Data Partner Relationships
    partners = Relationship(
        'backend.database.models.partner.Partner',
        "MEMBER_OF_PARTNER", model=PartnerMember)
    received_invitations = Relationship(
        'backend.database.models.partner.Invitation',
        "RECIEVED")
    extended_invitations = Relationship(
        'backend.database.models.partner.Invitation',
        "EXTENDED")
    entended_staged_invitations = Relationship(
        'backend.database.models.partner.StagedInvitation',
        "EXTENDED")

    def verify_password(self, pw: str) -> bool:
        """
        Verify the user's password using bcrypt.
        Args:
            pw (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        # return bcrypt.checkpw(pw.encode("utf8"), self.password.encode("utf8"))
        return check_password_hash(self.password_hash, pw)

    def set_password(self, pw: str):
        """
        Set the user's password.
        Args:
            pw (str): The password to set.
        """
        self.password_hash = User.hash_password(pw)

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
        # return bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt()).decode("utf8")
        return generate_password_hash(pw)

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
