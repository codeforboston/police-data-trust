import os
from dotenv import load_dotenv
from datetime import timedelta

if os.environ.get("FLASK_ENV") != "production":
    load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(64))
    JWT_TOKEN_LOCATION = os.environ.get(
        "JWT_TOKEN_LOCATION", ["headers", "cookies"]
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    TOKEN_EXPIRATION = timedelta(
        hours=os.environ.get("TOKEN_EXPIRATION_HOURS", 12)
    )
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "police_data")

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = bool(os.environ.get("MAIL_USE_SSL"))
    MAIL_USE_TLS = bool(os.environ.get("MAIL_USER_TLS"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "National Police Data Coalition <{email}>".format(email=MAIL_USERNAME),
    )

    # Flask-User settings
    USER_APP_NAME = (
        "Police Data Trust"  # Shown in and email templates and page footers
    )
    USER_ENABLE_EMAIL = True  # Enable email authentication
    USER_ENABLE_USERNAME = True  # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@policedatatrust.com"

    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return "postgresql://%s:%s@%s:%s/%s" % (
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    FLASK_DB_SEEDS_PATH = "alembic/seeds.py"


class DevelopmentConfig(Config):
    ENV = "development"
    # Use fixed secrets in development so tokens work across server restarts
    SECRET_KEY = os.environ.get("SECRET_KEY", "my-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "my-jwt-secret-key")


class ProductionConfig(Config):
    """Config designed for Heroku CLI deployment."""

    ENV = "production"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

    # @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #     return os.environ.get("DATABASE_URL")


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    POSTGRES_DB = "police_data_test"
    SECRET_KEY = "my-secret-key"
    JWT_SECRET_KEY = "my-jwt-secret-key"


def get_config_from_env(env: str) -> Config:
    """This function takes a string variable, looks at what that string variable
    is, and returns an instance of a Config class corresponding to that string
    variable.

    Args:
        env: (str) A string. Usually this is from `app.env` inside of the
             `create_app` function, which in turn is set by the environment
             variable `FLASK_ENV`.
    Returns:
        A Config instance corresponding with the string passed.

    Example:
        >>> get_config_from_env('development')
        DevelopmentConfig()
    """
    config_mapping = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "testing": TestingConfig,
    }
    try:
        config = config_mapping[env]
    except KeyError:
        print(
            f"Bad config passed."
            f"The config must be in {config_mapping.keys()}"
        )
        raise
    else:
        return config()
