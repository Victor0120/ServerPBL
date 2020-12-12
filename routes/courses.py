from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from server import db
from models import User as UserTable, Course as CourseTable, CourseScheme, CourseQuestionScheme, CourseQuestionAnswerScheme


courses = Blueprint('courses', __name__, url_prefix='/courses')


class Courses():

  @jwt_required
  def get_user_courses():
    try:
      user_id = get_jwt_identity()
      user = UserTable.query.get(user_id)
      teacher = user.teacher

      if teacher:
        courses = teacher.courses
      else:
        courses = user.courses

      course_scheme = CourseScheme()
      output = course_scheme.dump(courses, many=True)

      return jsonify({"courses": output})

    except Exception as e:
      return str(e), 400

  @jwt_required
  def get_all_courses():
    courses = CourseTable.query.all()

    course_schema = CourseScheme()
    output = course_schema.dump(courses, many=True)

    return jsonify({"courses":output})

  @jwt_required
  def get_course_questions():
    try:
      user_id = get_jwt_identity()
      teacher = UserTable.query.get(user_id).teacher

      if not teacher:
        return "Unauthorized", 401

      course_question_scheme = CourseQuestionScheme()
      course_scheme = CourseScheme()

      if 'id' in request.json:
        course_id = request.json['id']

        course = CourseTable.query.get(course_id)
        course_questions = course.course_questions

        results = course_question_scheme.dump(course_questions, many=True)
        course = course_scheme.dump(course)

        for res in results:
          res['course'] = course

      else:
        results = []
        for course in teacher.courses:
          course_questions = course_question_scheme.dump(course.course_questions, many=True)

          course = course_scheme.dump(course)
          for question in course_questions:
            question['course'] = course

          results.extend(course_questions)

      return jsonify({"questions": results})

    except Exception as e:
      return str(e), 400


  @jwt_required
  def get_course_question_answers():
    try:
      course_id = request.json['id']

      course = CourseTable.query.get(course_id)
      course_questions_answers = course.course_questions_answers

      course_question_answer_scheme = CourseQuestionAnswerScheme()
      output = course_question_scheme.dump(course_questions_answers, many=True)

      return jsonify({"question_answers": output})
    except Exception as e:
      return str(e), 400


courses.add_url_rule('/', view_func=Courses.get_user_courses, methods=['GET'])  
courses.add_url_rule('/questions/', view_func=Courses.get_course_questions, methods=['POST'])
courses.add_url_rule('/question-answers/', view_func=Courses.get_course_question_answers, methods=['POST'])

