from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.incidents import incident_routes
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["PDT_DB_URI"]
db = SQLAlchemy(app)

@app.before_first_request
def setup_application() -> None:
    """Do initial setup of application."""
    db.create_all()

@app.route('/')
def hello_world():
        return 'Hello, World!'

db.init_app(app)
app.register_blueprint(incident_routes)
app.run()