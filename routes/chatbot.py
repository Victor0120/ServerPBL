import requests

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from server import db
from models import QAModel, Course

chatbot = Blueprint('chatbot', __name__, url_prefix='/chatbot')


class Chatbot():
  @jwt_required
  def chat():
      if request.method == 'POST':
        course_id = request.json['course_id']
        question = request.json['question']

        course = Course.query.get(course_id)
        doc_model = course.faq_model_id
        faq_model = course.doc_model_id

        json_data = {
            'sample': 'sample'
        }

        resonse = get_answer(question, course_id, 3)

        if faq_qa:
            r = requests.post(url=model_endpoint, json=json_data).json()

            answers = r[0]['answers']

            for answer in answers:
                if answer['probability'] > 80:


        r = requests.post(url=model_endpoint, json=json_data).json()

 
 
chatbot.add_url_rule('/', view_func=, methods=['GET', 'POST'])  

