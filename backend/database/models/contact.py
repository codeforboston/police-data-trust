from backend.schemas import JsonSerializable

from neomodel import (
    StructuredNode, StringProperty, EmailProperty, DateTimeProperty, BooleanProperty, db
)


class EmailContact(StructuredNode, JsonSerializable):
    email = EmailProperty(required=True, unique_index=True)
    confirmed = BooleanProperty(default=False)
    email_confirmed_at = DateTimeProperty()

    @classmethod
    def get_or_create(cls, email_address: str) -> "EmailContact":
        query = """
        MERGE (e:EmailContact {email: $email})
        ON CREATE SET e.confirmed = false
        RETURN e
        """
        rows, _ = db.cypher_query(query, {"email": email_address})
        return cls.inflate(rows[0][0])


class PhoneContact(StructuredNode, JsonSerializable):
    phone_number = StringProperty(required=True, unique_index=True)

    @classmethod
    def get_or_create(cls, phone_number: str) -> "PhoneContact":
        query = """
        MERGE (p:PhoneContact {phone_number: $phone_number})
        RETURN p
        """
        rows, _ = db.cypher_query(query, {"phone_number": phone_number})
        return cls.inflate(rows[0][0])


class SocialMediaContact(StructuredNode, JsonSerializable):
    twitter_url = StringProperty()
    linkedin_url = StringProperty()
    facebook_url = StringProperty()
    instagram_url = StringProperty()
    youtube_url = StringProperty()
    tiktok_url = StringProperty()