from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..database import User, EmailContact, SocialMediaContact, PhoneContact

bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@bp.route("/self", methods=["GET"])
@cross_origin()
@jwt_required()
def get_current_user():
    """Return the currently authenticated user's full profile"""
    uid = get_jwt_identity()

    try:
        user = User.nodes.get(uid=uid)
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404

    primary_email = user.email
    additional_emails = [e.email for e in user.secondary_emails.all()]
    phone_numbers = [p.phone_number for p in user.phone_contacts.all()]

    sm = user.social_media_contacts.single()
    social_media = {}
    if sm:
        social_media = {
            "twitter_url": getattr(sm, "twitter_url", None),
            "facebook_url": getattr(sm, "facebook_url", None),
            "linkedin_url": getattr(sm, "linkedin_url", None),
            "instagram_url": getattr(sm, "instagram_url", None),
            "youtube_url": getattr(sm, "youtube_url", None),
            "tiktok_url": getattr(sm, "tiktok_url", None),
        }

    payload = {
        "uid": user.uid,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "primary_email": primary_email,
        "contact_info": {
            "additional_emails": additional_emails,
            "phone_numbers": phone_numbers,
        },
        "website": user.website,
        "location": {
            "city": user.city,
            "state": user.state,
        },
        "employment": {
            "employer": user.organization,
            "title": user.title,
        },
        "bio": user.biography,
        "profile_image": None,  # placeholder image for now
        "social_media": social_media,
    }

    return jsonify(payload), 200


@bp.route("/self", methods=["PATCH", "OPTIONS"])
@cross_origin()
@jwt_required()
def update_current_user():
    """Update current user profile"""
    uid = get_jwt_identity()
    user = User.nodes.get(uid=uid)
    data = request.get_json() or {}

    for field in ["first_name", "last_name", "bio"]:
        if field in data:
            setattr(user, {"bio": "biography"}.get(field, field), data[field])

    if "primary_email" in data:
        new_email = data["primary_email"]
        if new_email:
            email_contact = EmailContact.get_or_create(new_email)
            existing_email = user.primary_email.single()
            if existing_email:
                user.primary_email.reconnect(existing_email, email_contact)
            else:
                user.primary_email.connect(email_contact)

    contact_info = data.get("contact_info", {})

    secondary_emails = contact_info.get("additional_emails", [])
    user.secondary_emails.disconnect_all()

    for email in secondary_emails:
        if email:
            contact = EmailContact.get_or_create(email)
            user.secondary_emails.connect(contact)

    phone_numbers = contact_info.get("phone_numbers", [])
    if phone_numbers:
        user.phone_contacts.disconnect_all()
        for phone in phone_numbers:
            if phone:
                phone_contact = PhoneContact.get_or_create(phone)
                user.phone_contacts.connect(phone_contact)

    if "website" in data:
        user.website = data["website"]

    location = data.get("location", {})
    if location.get("city"):
        user.city = location["city"]
    if location.get("state"):
        user.state = location["state"]

    employment = data.get("employment", {})
    if employment.get("employer"):
        user.organization = employment["employer"]
    if employment.get("title"):
        user.title = employment["title"]

    social_media = data.get("social_media", {})
    if social_media:
        existing_sm = user.social_media_contacts.single()
        if existing_sm:
            for k, v in social_media.items():
                if v is not None:
                    setattr(existing_sm, k, v)
            existing_sm.save()
        else:
            new_sm = SocialMediaContact(**social_media).save()
            user.social_media_contacts.connect(new_sm)

    user.save()

    return get_current_user()
