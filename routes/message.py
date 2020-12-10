from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from models import Message as MessageTable, User as UserTable, MessageScheme
from server import db


messages = Blueprint('messages', __name__, url_prefix='/messages')


class Message():
  
  @jwt_required
  def get_user_messages():
    try:
      user_id = get_jwt_identity()
      user = UserTable.query.get(user_id['id'])

    except Exception as e:
      return str(e)

    # user not in database
    if not user:
      return 'User not registered', 401

    messages = MessageTable.query.filter((MessageTable.sender_id==user_id) | (MessageTable.receiver_id==user_id)).all()

    message_schema = MessageScheme()
    data = message_schema.dump(messages)

    return jsonify({'messages': data})
  
  @jwt_required
  def post_user_message():
    try:
      message = request.json['message']
      course_id = request.json['course_id']

      sender_id = get_jwt_identity()
      receiver_id = current_app.config['CHATBOT_ID']
      
      newMessage = MessageTable(sender_id=sender_id["id"], course_id=course_id, receiver_id=receiver_id, message=message)

      db.session.add(newMessage)   
      db.session.commit()

      message_schema = MessageScheme()
      data = message_schema.dump(newMessage)

      return jsonify({"status" : "success", "data": data}), 200
    
    except Exception as e:
      return str(e), 400

messages.add_url_rule('/', view_func=Message.get_user_messages, methods=['GET'])
messages.add_url_rule('/', view_func=Message.post_user_message, methods=['POST'])

