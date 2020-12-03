from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

import auth

from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beepboop.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from tables import User, User_Courses, Teacher, Teacher_Courses, Courses, Course_Questions, Course_Question_Answer, Course_Materials, Message_History


def create_app():
	
	app.config['JWT_SECRET_KEY'] = 'beep-boop'
	
	
	JWTManager(app)




	load_dotenv('./.env')
	CORS(app)

	app.register_blueprint(auth.auth)

	if __name__ == "__main__":
		app.run(debug=True)

	return app
