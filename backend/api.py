from flask import Flask

from backend.routes.incidents import incident_routes
from backend.config import Config
from backend.incidents import db


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = Config()
    app.config.from_object(config)

    db.init_app(app)

    app.register_blueprint(incident_routes)

    @app.before_first_request
    def setup_application() -> None:
        """Do initial setup of application."""
        db.create_all()

    @app.route("/")
    def hello_world():
        return "Hello, world!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
