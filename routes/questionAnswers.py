from flask import Blueprint, request, jsonify, current_app

from flask_jwt_extended import jwt_required

from server import db
from models import CourseQuestionAnswer, CourseQuestion

question_answer = Blueprint('question', __name__, url_prefix='/question-answer')


class QuestionAnswer():
  @jwt_required
  def post_answer():
    try:
        course_id = request.json['course_id']
        question_id = request.json['question_id']
        question = request.json['question']
        answer = request.json['answer']

        course_question_answer = CourseQuestionAnswer(course_id=course_id, question=question, answer=answer)
        question = CourseQuestion.query.get(question_id)
        if question:
            db.session.delete(question)
        
        db.session.add(course_question_answer)
        db.session.commit()

        return jsonify({'status': 'success'}), 200 #TODO return the posted answer

    except Exception as e:
        return str(e), 400
 
  @jwt_required
  def post_question_and_answer():
      try:
        course_id = request.json['course_id']
        question = request.json['question']
        answer = request.json['answer']

        course_question_answer = CourseQuestionAnswer(course_id=course_id, question=question, answer=answer)
        db.session.add(course_question_answer)
        db.session.commit()

        return jsonify({'status': 'success'}), 200  #TODO return the posted answer
        
      except Exception as e:
          return str(e), 400

question_answer.add_url_rule('/answer/', view_func=QuestionAnswer.post_answer, methods=['POST'])
question_answer.add_url_rule('/', view_func=QuestionAnswer.post_question_and_answer, methods=['POST'])