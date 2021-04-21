import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))

    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_USER = os.environ.get(
        "POSTGRES_USER", os.environ.get("USER", "postgres")
    )
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "police_data")

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


class DevelopmentConfig(Config):
    ENV = "development"


class ProductionConfig(Config):
    """Config designed for Heroku CLI deployment."""

    ENV = "production"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return os.environ.get("DATABASE_URL")


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    POSTGRES_DB = "police_data_test"


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
