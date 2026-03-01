from flask import Blueprint, jsonify, request, send_from_directory
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from werkzeug.utils import secure_filename
PROFILE_PIC_FOLDER=os.getenv("PROFILE_PIC_FOLDER")

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
        "profile_image": user.profile_image,
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

    profile_image = data.get("profile_image")
    if profile_image:
        user.profile_image = profile_image

    user.save()

    return get_current_user()


@bp.route("/self/upload-profile-image", methods=["POST"])
@cross_origin()
@jwt_required()
def upload_profile_image():
    """Update current user profile image"""
    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400

    file = request.files["file"]

    if not file or not file.filename:
        return jsonify({"error": "Empty file"}), 400

    # Fetch user
    uid = get_jwt_identity()
    try:
        user = User.nodes.get(uid=uid)
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404

    try:
        url = save_profile_photo(file, user_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Update Neo4j
    user.profile_image = url
    user.save()

    return jsonify({"profile_image_url": url}), 200


def save_profile_photo(file, user_id):
    """
    Saves file locally or to S3 depending on environment.
    Returns the URL to store in Neo4j.
    """
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    if not ext:
        raise ValueError("File must have an extension")

    # ---------- LOCAL ----------
    if os.environ.get("FLASK_ENV") != "production":
        upload_dir = PROFILE_PIC_FOLDER
        os.makedirs(upload_dir, exist_ok=True)

        filename = f"user_{user_id}{ext}"
        path = os.path.join(upload_dir, filename)

        file.save(path)

        return f"Uploaded Successfully to {path}"
    else:
        raise NotImplementedError("Production profile photo upload not implemented")
    # ---------- PRODUCTION (S3) ----------
    # else:
    #     import boto3

    #     s3 = boto3.client("s3")
    #     bucket = current_app.config["S3_BUCKET"]

    #     key = f"profile_photos/user_{user_id}_{uuid.uuid4().hex}{ext}"

    #     s3.upload_fileobj(
    #         file,
    #         bucket,
    #         key,
    #         ExtraArgs={
    #             "ContentType": file.mimetype,
    #             "ACL": "private",
    #         },
    #     )

    #     # store S3 path, not signed URL
    #     return f"s3://{bucket}/{key}"


@bp.route("/self/profile-image", methods=["GET"])
@jwt_required()
def get_profile_photo():
    user_id = get_jwt_identity()
    try:
        user = User.nodes.get(uid=user_id)
    except User.DoesNotExist:
        return {"error": "User not found"}, 404
    if not user or not user.profile_image:
        return {"error": "No profile photo"}, 404

    # import boto3
    from urllib.parse import urlparse
    import os

    if os.environ.get("FLASK_ENV") != "production":
        # local dev
        filename = os.path.basename(user.profile_image)
        directory = PROFILE_PIC_FOLDER
        return send_from_directory(directory, filename)
    else:
        raise NotImplementedError("Production profile photo upload not implemented")
        parsed = urlparse(user.profile_photo_url)
        bucket = parsed.netloc
        key = parsed.path.lstrip("/")

        s3 = boto3.client("s3")
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600,  # 1 hour
        )
        return {"profile_image_url": url}, 200
