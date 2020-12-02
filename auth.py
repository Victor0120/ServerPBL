from flask import Blueprint, request, jsonify
from os import environ
from random import randint

from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from threading import Timer

from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__, url_prefix='/auth')

FROM_EMAIL = 'beepboop.faf@gmail.com'
TIME_CODE_IS_VALID = 300 #code will be valid 5 min

codeList = []


@auth.route('/', methods=['POST'])
def postEmail(): 
  if request.method == 'POST':
    return sendEmailMessage()


def sendEmailMessage():
  email = request.json['email']

  # create Mail object
  message = Mail(from_email=FROM_EMAIL, to_emails=[email])

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

    timer = Timer(TIME_CODE_IS_VALID, deleteCode, [email])
    timer.start()
    
    return str(response.status_code)

  except Exception as e:
    print("Error: {0}".format(e))
    return str(e), 401


def deleteCode(email):
  next(codeList.remove(item) for item in codeList if item["email"] == email)


@auth.route('/code/', methods=['POST'])
def postCode():
  email = request.json['email']
  code = request.json['code']
  
  for item in codeList:
    if item['email'] == email and item['code'] == int(code):
      codeList.remove(item)
      access_token = create_access_token(identity=email)
      return jsonify(access_token=access_token), 200

  return 'Wrong code!', 401