from backend.schemas import JsonSerializable
from neomodel import (
    StringProperty,
    UniqueIdProperty,
    StructuredNode,
    DateProperty
)


class Attachment(JsonSerializable, StructuredNode):
    """
    Multimedia attachment.
    """
    __property_order__ = [
        "uid", "title", "url", "filetype"
    ]
    __hidden_properties__ = ["hash"]

    uid = UniqueIdProperty()
    title = StringProperty()
    hash = StringProperty()
    url = StringProperty()
    filetype = StringProperty()


class Article(StructuredNode, JsonSerializable):
    """
    News article.
    """

    uid = UniqueIdProperty()
    title = StringProperty()
    publisher = StringProperty()
    publication_date = DateProperty()
    url = StringProperty()


class SocialMediaInfo(StructuredNode, JsonSerializable):
    """
    Social media information.
    """
    __property_order__ = [
        "twitter_url", "linkedin_url", "facebook_url",
        "instagram_url", "youtube_url", "tiktok_url"
    ]

    twitter_url = StringProperty()
    linkedin_url = StringProperty()
    facebook_url = StringProperty()
    instagram_url = StringProperty()
    youtube_url = StringProperty()
    tiktok_url = StringProperty()
