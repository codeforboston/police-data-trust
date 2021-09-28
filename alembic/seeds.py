from flask import current_app as app
from backend.database.core import db

if app.env == "development":
    import alembic.dev_seeds
elif app.env == "production":
    import alembic.prod_seeds
