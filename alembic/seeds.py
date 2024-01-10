from flask import current_app as app

if app.env == "development":
    pass
elif app.env == "production":
    pass
