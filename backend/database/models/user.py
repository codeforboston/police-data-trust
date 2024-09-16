"""Define the SQL classes for Users."""

import bcrypt
from backend.database.core import db
from backend.database import JsonSerializable, PropertyEnum
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
    uid = UniqueIdProperty()
    active = BooleanProperty(default=True)

    # User authentication information. The collation="NOCASE" is required
    # to search case insensitively when USER_IFIND_MODE is "nocase_collation".
    email = EmailProperty(required=True, unique_index=True)
    email_confirmed_at = DateProperty()
    password = StringProperty(required=True)

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

    def verify_password(self, pw: str) -> bool:
        """
        Verify the user's password using bcrypt.
        Args:
            pw (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return bcrypt.checkpw(pw.encode("utf8"), self.password.encode("utf8"))

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
