from flask import Blueprint, request, jsonify, current_app
from os import environ
from random import randint
from threading import Timer

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_cors import cross_origin

from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from server import db
from models import User, CourseQuestionAnswer, CourseQuestion

question_answer = Blueprint('question', __name__, url_prefix='/question-answer')

codeList = []

class QuestionAnswer():
  def handleAnswerSubmit():
    try:
        course_id = request.json['course_id']
        question_id = request.json['question_id']
        question = request.json['question']
        answer = request.json['answer']

        question_answer = CourseQuestionAnswer(course_id=course_id, question=question, answer=answer)
        question = CourseQuestion.query.get(question_id)
        if question:
            db.session.delete(question)
        
        db.session.add(question_answer)
        db.session.commit()

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return str(e), 400



question_answer.add_url_rule('/', view_func=QuestionAnswer.handleAnswerSubmit, methods=['POST'])