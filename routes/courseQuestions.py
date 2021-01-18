from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import CourseQuestion, CourseQuestionScheme
from server import db
from utils import get_answers

course_questions = Blueprint('course_questions', __name__, url_prefix='/course-questions')


class CourseQuestions():

  @jwt_required
  def post_question():
    user_id = get_jwt_identity()
    message = request.json['message']
    course_id = request.json['course_id']
    
    course_question_scheme = CourseQuestionScheme()
    course_question = CourseQuestion(sender_id=user_id, course_id=course_id, message=message)
    db.session.add(course_question)   
    db.session.commit()

    return jsonify({"status" : "success"}), 200


course_questions.add_url_rule('/', view_func=CourseQuestions.post_question, methods=['POST'])

