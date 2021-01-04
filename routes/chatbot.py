import requests

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from server import db


chatbot = Blueprint('chatbot', __name__, url_prefix='/chatbot')


class Courses():
  @jwt_required
  def chat():
      if request.method == 'POST':
          course_id = request.json['course_id']
          question = request.json['question']

          json_data = {
              'sample': 'sample'
          }

          r = requests.post(url=model_endpoint, json=json_data).json()

          return r["predictions"][0][0]


courses.add_url_rule('/', view_func=, methods=['GET', 'POST'])  

