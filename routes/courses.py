from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from server import db
from models import User as UserTable, Course as CourseTable, CourseScheme, CourseQuestionScheme, CourseQuestionAnswerScheme, Teacher as TeacherTable, TeacherScheme, UserScheme


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
      courses_output = course_scheme.dump(courses, many=True)

      return jsonify({"courses": courses_output})

    except Exception as e:
      return str(e), 400

  @jwt_required
  def get_all_courses():
    courses = CourseTable.query.all()

    course_schema = CourseScheme()
    teachers_schema = TeacherScheme()
    user_scheme = UserScheme()

    output = []

    for course in courses:
      teachers = course.teachers

      course_output = course_schema.dump(course)
      teachers_output = teachers_schema.dump(teachers, many=True)

      teacher_email_list = []
      for teacher in teachers_output:
        teacher_details = UserTable.query.get(teacher['user_id'])
        teacher_output = user_scheme.dump(teacher_details)

        teacher_email_list.append(teacher_output["email"])

      course_output["teachers"] = teacher_email_list
      output.append(course_output)

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


courses.add_url_rule('/', view_func=Courses.get_all_courses, methods=['GET'])  
courses.add_url_rule('/user-courses/', view_func=Courses.get_user_courses, methods=['GET'])  
courses.add_url_rule('/questions/', view_func=Courses.get_course_questions, methods=['POST'])
courses.add_url_rule('/question-answers/', view_func=Courses.get_course_question_answers, methods=['POST'])

