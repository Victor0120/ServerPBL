from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os

from models import db
from models import Course, Teacher, User, CourseQuestion, TeacherCourse
from models import Course as CourseTable, CourseScheme
from models import CourseQuestionScheme, CourseQuestionAnswerScheme

course_materials = Blueprint('course-materials', __name__, url_prefix='/course-materials')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

class CourseMaterials():

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @jwt_required
    def uploadFiles():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        teacher = user.teacher

        if (not teacher):
            return "Forbidden", 403

        files = request.files.getlist('files')
        course_id = request.form['id']

        if (not files):
            return 'No files', 400

        for file in files:
            if file and CourseMaterials.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                dir = os.path.join('static', 'course', 'materials', course_id)
                if not os.path.exists(dir):
                    os.makedirs(dir)

                file.save(os.path.join(dir, filename))


        return "Success", 200


#courses.add_url_rule('/',view_func=Courses.get_all_courses, methods=['GET'])
course_materials.add_url_rule('/', view_func=CourseMaterials.uploadFiles, methods=['POST'])  
