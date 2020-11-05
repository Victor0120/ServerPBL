from flask import Blueprint, request

import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

auth = Blueprint('auth', __name__, url_prefix='/auth')

FROM_EMAIL = 'beepboop.faf@gmail.com'

TEMPLATE_ID = 'd-6b6d8549c1774c7688d71520cbb9136b'

@auth.route('/', methods=['POST'])
def postEmail(): 
  if request.method == 'POST':
    return sendEmailMessage()


def sendEmailMessage():
  email = request.json['email']

  # create Mail object
  message = Mail(
          from_email=FROM_EMAIL,
          to_emails=[email])

  # pass custom values for HTML placeholders
  message.dynamic_template_data = {
    'verification_code': 123456
  }

  message.template_id = TEMPLATE_ID

  try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)

  except Exception as e:
    print("Error: {0}".format(e))

  return str(response.status_code)