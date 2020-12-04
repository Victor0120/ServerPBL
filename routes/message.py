from flask import Blueprint, jsonify
from models import Message as MessageTable
from models import MessageScheme
from models import User as UserTable
from models import MessageSchema
from server import db

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


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

    messages = Message.query.filter((Message.sender_id==user_id) | (Message.receiver_id==user_id)).all()
    message_schema = MessageScheme()

    return jsonify({'messages': messages})


messages.add_url_rule('/', view_func=Message.get_user_messages(), methods=['GET'])


