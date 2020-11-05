from flask import Flask

import auth

def create_app():
	app = Flask(__name__)

	app.register_blueprint(auth.auth)

	if __name__ == "__main__":
		app.run(debug=True)

	return app
