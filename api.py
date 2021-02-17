from flask import Flask
from routes.incidents import incident_routes;
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

app.register_blueprint(incident_routes)
app.run()