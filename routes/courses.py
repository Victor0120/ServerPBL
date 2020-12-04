from flask import Blueprint, jsonify

from models import Course as CourseTable, CourseScheme

courses = Blueprint('courses', __name__, url_prefix='/courses')


class Courses():
  def get_all_courses():
    courses = CourseTable.query.all()

    course_schema = CourseScheme()
    output = course_schema.dump(courses, many=True)

    return jsonify({"courses":output})

courses.add_url_rule('/',view_func=Courses.get_all_courses, methods=['GET'])
