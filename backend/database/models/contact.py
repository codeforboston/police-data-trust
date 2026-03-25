from backend.schemas import JsonSerializable

from neomodel import (
    StructuredNode, StringProperty, EmailProperty,
    DateTimeNeo4jFormatProperty, BooleanProperty, db
)


class EmailContact(StructuredNode, JsonSerializable):
    email = EmailProperty(required=True, unique_index=True, max_length=255)
    confirmed = BooleanProperty(default=False)
    email_confirmed_at = DateTimeNeo4jFormatProperty()

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
    phone_number = StringProperty(
        required=True, unique_index=True, max_length=20)

    @classmethod
    def get_or_create(cls, phone_number: str) -> "PhoneContact":
        query = """
        MERGE (p:PhoneContact {phone_number: $phone_number})
        RETURN p
        """
        rows, _ = db.cypher_query(query, {"phone_number": phone_number})
        return cls.inflate(rows[0][0])


class SocialMediaContact(StructuredNode, JsonSerializable):
    twitter_url = StringProperty(max_length=255)
    linkedin_url = StringProperty(max_length=255)
    facebook_url = StringProperty(max_length=255)
    instagram_url = StringProperty(max_length=255)
    youtube_url = StringProperty(max_length=255)
    tiktok_url = StringProperty(max_length=255)
