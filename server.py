from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow

from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)
	
  load_dotenv('./.env')

  db.init_app(app)
  migrate.init_app(app, db, render_as_batch=True)

  JWTManager(app)
  CORS(app)

  from routes import user, courses, message, courseMaterials, questionAnswers, courseQuestions

  app.register_blueprint(user.user)
  app.register_blueprint(courses.courses)
  app.register_blueprint(message.messages)

  app.register_blueprint(questionAnswers.question_answer)
  app.register_blueprint(courseMaterials.course_materials)
  app.register_blueprint(courseQuestions.course_questions)

  return app
