from flask import Flask, redirect, render_template, session, request, flash
from flask_login import login_required

from backend.routes.incidents import incident_routes
from backend.config import Config
from backend.incidents import db
from backend.cli import pip_compile


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = Config()
    app.config.from_object(config)

    db.init_app(app)
    app.register_blueprint(incident_routes)
    app.cli.add_command(pip_compile)

    @app.before_first_request
    def setup_application() -> None:
        """Do initial setup of application."""
        db.create_all()

    @app.route("/")
    @login_required
    def hello_world():
        """Hello World Page."""
        return "Hello, world!"

    return app
    


if __name__ == "__main__":
    app = create_app()
    app.run()
