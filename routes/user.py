from flask import Blueprint, request, jsonify, current_app
from os import environ
from random import randint
from threading import Timer

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from server import db
from models import User as UserTable, Teacher as TeacherTable, Course as CourseTable, CourseScheme

user = Blueprint('user', __name__, url_prefix='/user')

codeList = []

class User():
  @jwt_required
  def get_user():
    try:
      user_id = get_jwt_identity()
      user = UserTable.query.get(user_id)
      is_admin = (user.teacher != None)

    except Exception as e:
      return str(e)

    return jsonify({'email': user.email, "isAdmin": is_admin}), 200

  def send_auth_email():
    email = request.json['email']

    # create Mail object
    message = Mail(from_email=current_app.config['CHATBOT_EMAIL'], to_emails=[email])

    VERIFICATION_CODE = randint(100000, 999999)

    # pass custom values for HTML placeholders
    message.dynamic_template_data = {
      'verification_code': VERIFICATION_CODE
    }

    message.template_id = environ.get('MESSAGE_TEMPLATE_ID')

    try:
      sg = SendGridAPIClient(environ.get('SENDGRID_API_KEY'))

      response = sg.send(message)

      codeList.append({
        "email": email,
        "code": VERIFICATION_CODE
      })

      def deleteCode(email):
        codeList = [item for item in codeList if item['email'] != email]

      timer = Timer(current_app.config['TIME_AUTH_CODE_IS_VALID'], deleteCode, [email])
      timer.start()
      
      return str(response.status_code)

    except Exception as e:
      print("Error: {0}".format(e))
      return str(e), 401
      
  def check_auth_code():
    email = request.json['email']
    code = request.json['code']
    
    for item in codeList:
      if item['email'] == email and item['code'] == int(code):
        codeList.remove(item)

        user = UserTable.query.filter_by(email=email).first()

        if user:
          access_token = create_access_token(identity=user.id, expires_delta=False)
          
          return jsonify(access_token=access_token), 200

        newUser = UserTable(email = email)

        db.session.add(newUser)   
        db.session.commit()

        access_token = create_access_token(identity=newUser.id)
        return jsonify(access_token=access_token), 200

    return 'Wrong code!', 401

  @jwt_required
  def add_course_to_user():
    try:
      courseId = request.json['course_id']
      
      userId = get_jwt_identity()
      user = UserTable.query.get(userId)
      
      course = CourseTable.query.get(courseId)
      user.courses.append(course)
      db.session.commit()

      course_schema = CourseScheme()
      output = course_schema.dump(course)

      return jsonify({'status': 'success', "course": output}), 200

    except Exception as e:
      return jsonify({'status': str(e)})

  @jwt_required
  def remove_user_course():
    try:
      courseId = request.args.get('course_id')

      userId = get_jwt_identity()
      user = UserTable.query.get(userId)

      course = CourseTable.query.get(courseId)

      user.courses.remove(course)
      db.session.commit()

      return jsonify({'status': 'success'}), 200
    
    except Exception as e:
      return jsonify({'status': str(e)})


user.add_url_rule('/',view_func=User.get_user, methods=['GET'])
user.add_url_rule('/course',view_func=User.add_course_to_user, methods=['POST'])
user.add_url_rule('/auth', view_func=User.send_auth_email, methods=['POST'])
user.add_url_rule('/auth/code',view_func=User.check_auth_code, methods=['POST'])
user.add_url_rule('/course', view_func=User.remove_user_course, methods=["DELETE"])
