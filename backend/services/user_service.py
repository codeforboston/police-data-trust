import os
import uuid
from urllib.parse import urlparse

import boto3
from flask import jsonify, send_from_directory
from werkzeug.utils import secure_filename

from backend.database import (
    EmailContact,
    PhoneContact,
    SocialMediaContact,
    User,
)
from backend.dto.user_profile import UpdateCurrentUser


class UserService:
    allowed_profile_photo_extensions = {".jpg", ".jpeg", ".png", ".gif"}

    def get_user_profile(self, user_uid: str) -> dict:
        user = User.nodes.get_or_none(uid=user_uid)
        if user is None:
            raise LookupError("User not found")
        return self.serialize_user_profile(user)

    def update_current_user_profile(
        self,
        user_uid: str,
        body: UpdateCurrentUser,
    ) -> dict:
        user = User.nodes.get_or_none(uid=user_uid)
        if user is None:
            raise LookupError("User not found")

        fields_set = body.model_fields_set

        if "first_name" in fields_set:
            user.first_name = body.first_name
        if "last_name" in fields_set:
            user.last_name = body.last_name
        if "bio" in fields_set:
            user.biography = body.bio
        if "website" in fields_set:
            user.website = body.website
        if "profile_image" in fields_set:
            user.profile_image = body.profile_image

        if "primary_email" in fields_set and body.primary_email:
            email_contact = EmailContact.get_or_create(body.primary_email)
            existing_email = user.primary_email.single()
            if existing_email:
                user.primary_email.reconnect(existing_email, email_contact)
            else:
                user.primary_email.connect(email_contact)

        if "contact_info" in fields_set and body.contact_info is not None:
            contact_fields = body.contact_info.model_fields_set

            if "additional_emails" in contact_fields:
                user.secondary_emails.disconnect_all()
                for email in body.contact_info.additional_emails or []:
                    if email:
                        user.secondary_emails.connect(
                            EmailContact.get_or_create(email)
                        )

            if "phone_numbers" in contact_fields:
                user.phone_contacts.disconnect_all()
                for phone in body.contact_info.phone_numbers or []:
                    if phone:
                        user.phone_contacts.connect(
                            PhoneContact.get_or_create(phone)
                        )

        if "location" in fields_set and body.location is not None:
            location_fields = body.location.model_fields_set
            if "city" in location_fields:
                user.city = body.location.city
            if "state" in location_fields:
                user.state = body.location.state

        if "employment" in fields_set and body.employment is not None:
            employment_fields = body.employment.model_fields_set
            if "employer" in employment_fields:
                user.organization = body.employment.employer
            if "title" in employment_fields:
                user.title = body.employment.title

        if "social_media" in fields_set and body.social_media is not None:
            social_media_fields = body.social_media.model_fields_set
            if social_media_fields:
                existing_sm = user.social_media_contacts.single()
                payload = body.social_media.model_dump(exclude_unset=True)
                if existing_sm:
                    for field, value in payload.items():
                        setattr(existing_sm, field, value)
                    existing_sm.save()
                else:
                    user.social_media_contacts.connect(
                        SocialMediaContact(**payload).save()
                    )

        user.save()
        return self.serialize_user_profile(user)

    def save_profile_photo(self, file, user_uid: str) -> str:
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()

        if not ext:
            raise ValueError("File must have an extension")
        if ext not in self.allowed_profile_photo_extensions:
            raise ValueError(f"Invalid file type: {ext}")

        if os.environ.get("FLASK_ENV") != "production":
            upload_dir = os.getenv("PROFILE_PIC_FOLDER")
            os.makedirs(upload_dir, exist_ok=True)

            path = os.path.join(upload_dir, f"user_{user_uid}{ext}")
            file.save(path)
            return path

        s3 = boto3.client("s3")
        bucket = os.getenv("S3_BUCKET")
        key = f"profile_photos/user_{user_uid}_{uuid.uuid4().hex}{ext}"

        s3.upload_fileobj(
            file,
            bucket,
            key,
            ExtraArgs={"ContentType": file.mimetype},
        )
        return f"s3://{bucket}/{key}"

    def update_profile_image(self, user_uid: str, file) -> dict:
        user = User.nodes.get_or_none(uid=user_uid)
        if user is None:
            raise LookupError("User not found")

        url = self.save_profile_photo(file, user_uid)
        user.profile_image = url
        user.save()

        return {"profile_image_url": url}

    def get_profile_photo(self, user_uid: str):
        user = User.nodes.get_or_none(uid=user_uid)
        if user is None:
            raise LookupError("User not found")
        if not user.profile_image:
            raise FileNotFoundError("No profile photo")

        if os.environ.get("FLASK_ENV") != "production":
            filename = os.path.basename(user.profile_image)
            directory = os.getenv("PROFILE_PIC_FOLDER")
            return send_from_directory(directory, filename)

        parsed = urlparse(user.profile_image)
        s3 = boto3.client("s3")
        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": parsed.netloc,
                "Key": parsed.path.lstrip("/"),
            },
            ExpiresIn=3600,
        )
        return jsonify({"profile_image_url": url}), 200

    @staticmethod
    def serialize_user_profile(user: User) -> dict:
        primary_email = user.email
        additional_emails = [e.email for e in user.secondary_emails.all()]
        phone_numbers = [p.phone_number for p in user.phone_contacts.all()]

        social_media = {}
        sm = user.social_media_contacts.single()
        if sm:
            social_media = {
                "twitter_url": getattr(sm, "twitter_url", None),
                "facebook_url": getattr(sm, "facebook_url", None),
                "linkedin_url": getattr(sm, "linkedin_url", None),
                "instagram_url": getattr(sm, "instagram_url", None),
                "youtube_url": getattr(sm, "youtube_url", None),
                "tiktok_url": getattr(sm, "tiktok_url", None),
            }

        return {
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
