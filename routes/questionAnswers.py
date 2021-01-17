from flask import Blueprint, request, jsonify, current_app

from flask_jwt_extended import jwt_required

from server import db
from models import CourseQuestionAnswer, CourseQuestion, CourseQuestionAnswerScheme

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

  @jwt_required
  def delete_question_answer():
    question_answer_id = request.args.get('question_answer_id')

    course_qa = db.session.query(CourseQuestionAnswer).get(question_answer_id)
    course_id = course_qa.course_id

    # # remove processed file from api
    # try:
    #   utils.delete_question_answer_from_api(question_answer_id, course_id)
    # except requests.exceptions.RequestException as err:
    #   return 'Error while deleting question/answer', 400
        
    # remove qa from db
    db.session.delete(course_qa)
    db.session.commit()

    return jsonify({"status" : "success"}), 200


  @jwt_required
  def get_question_answers(course_id):
      qa_scheme = CourseQuestionAnswerScheme()
      question_answers = CourseQuestionAnswer.query.filter_by(course_id=course_id).all()
      question_answers = qa_scheme.dump(question_answers, many=True)

      return jsonify({'question_answers': question_answers}), 200

  
  #@jwt_required
  def modify_answer():
    question_answer_id = request.json['question_answer_id']
    new_answer = request.json['new_answer']

    question_answer = CourseQuestionAnswer.query.get(question_answer_id)
    question_answer.answer = new_answer
    db.session.commit()

    return jsonify({'status': 'success'}), 200


question_answer.add_url_rule('/answer/', view_func=QuestionAnswer.post_answer, methods=['POST'])
question_answer.add_url_rule('/', view_func=QuestionAnswer.post_question_and_answer, methods=['POST'])
question_answer.add_url_rule('/', view_func=QuestionAnswer.modify_answer, methods=['PUT'])
question_answer.add_url_rule('/', view_func=QuestionAnswer.delete_question_answer, methods=['DELETE'])
question_answer.add_url_rule('/<int:course_id>', view_func=QuestionAnswer.get_question_answers, methods=['GET'])