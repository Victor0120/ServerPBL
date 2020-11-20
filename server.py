from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

import auth

def create_app():
	app = Flask(__name__)
	app.config['JWT_SECRET_KEY'] = 'beep-boop'
	JWTManager(app)

	load_dotenv('./.env')
	CORS(app)

	app.register_blueprint(auth.auth)

	if __name__ == "__main__":
		app.run(debug=True)

	return app
