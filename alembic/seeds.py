from flask import current_app as app

if app.env == "development":
    import alembic.dev_seeds
elif app.env == "production":
    import alembic.prod_seeds
