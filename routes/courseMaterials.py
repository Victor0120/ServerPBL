from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os, itertools

from models import db
from models import Course, Teacher, User, CourseQuestion, TeacherCourse
from models import Course as CourseTable, CourseScheme
from models import CourseMaterial, CourseMaterialScheme
from models import CourseQuestionScheme, CourseQuestionAnswerScheme

course_materials = Blueprint('course-materials', __name__, url_prefix='/course-materials')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

class CourseMaterials():

    def file_exists(filename):
        file = CourseMaterial.query.filter_by(filename=filename).first()

        return file != None

    def get_filename(filename):
        if not CourseMaterials.file_exists(filename):
            return filename

        pos = filename.rfind('.')
        name = filename[:pos]
        ext = filename[pos + 1:]

        for i in itertools.count(start=1):
            new_filename = name + '(' + str(i) + ').' + ext 

            if not CourseMaterials.file_exists(new_filename):
                return new_filename


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

        added_files = []
        for file in files:
            if file and CourseMaterials.allowed_file(file.filename):
                filename = CourseMaterials.get_filename(secure_filename(file.filename))

                dir = os.path.join('static', 'course', 'materials', course_id)
                if not os.path.exists(dir):
                    os.makedirs(dir)

                file.save(os.path.join(dir, filename))
                file_db = CourseMaterial(filename=filename, course_id=int(course_id))
                db.session.add(file_db)
                db.session.commit()
                added_files.append(filename)

        return jsonify({
            'filenames': added_files,
            'status':  "not saved" if len(added_files) == 0 else 'success'
            }
        )

course_materials.add_url_rule('/', view_func=CourseMaterials.uploadFiles, methods=['POST'])  
