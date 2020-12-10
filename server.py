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
  migrate.init_app(app, db)

  JWTManager(app)
  CORS(app)

  from routes import user, courses, message
  app.register_blueprint(user.user)
  app.register_blueprint(courses.courses)
  app.register_blueprint(message.messages)

  return app
