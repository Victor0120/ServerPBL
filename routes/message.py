from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import Message as MessageTable, User as UserTable, MessageScheme
from server import db
from utils import get_answers

messages = Blueprint('messages', __name__, url_prefix='/messages')


class Message():
  
  @jwt_required
  def get_user_messages():
    try:
      user_id = get_jwt_identity()
      user = UserTable.query.get(user_id)

    except Exception as e:
      return str(e)

    # user not in database
    if not user:
      return 'User not registered', 401

    messages = MessageTable.query.filter((MessageTable.sender_id==user_id) | (MessageTable.receiver_id==user_id)).all()

    message_schema = MessageScheme()
    data = message_schema.dump(messages, many=True)

    return jsonify({'messages': data})
  
  @jwt_required
  def post_user_message():
    try:
      message = request.json['message']
      course_id = request.json['course_id']
      user_id = get_jwt_identity()
      bot_id = current_app.config['CHATBOT_ID']
      
      message_schema = MessageScheme()
      input_message = MessageTable(sender_id=user_id, course_id=course_id, receiver_id=bot_id, message=message)
      db.session.add(input_message)   
      db.session.commit()
      
      answers = get_answers(message, course_id, 1)
      new_messages = []
      
      for answer in answers:
        answer_message = MessageTable(sender_id=bot_id, course_id=course_id, receiver_id=user_id, message=answer['message'])
        new_messages.append(message_schema.dump(answer_message))

        db.session.add(answer_message)
        db.session.commit()


      return jsonify({"status" : "success", "messages": new_messages}), 200
    
    except Exception as e:
      return str(e), 400

messages.add_url_rule('/', view_func=Message.get_user_messages, methods=['GET'])
messages.add_url_rule('/', view_func=Message.post_user_message, methods=['POST'])

