from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    # Retrieve all messages ordered by created_at in ascending order
    messages = Message.query.order_by(Message.created_at).all()
    # Serialize messages to JSON
    message_list = [message.serialize() for message in messages]
    return jsonify(message_list)

@app.route('/messages', methods=['POST'])
def create_message():
    # Get data from request JSON
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')
    # Create a new message
    new_message = Message(body=body, username=username, created_at=datetime.now())
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    # Get data from request JSON
    data = request.get_json()
    new_body = data.get('body')
    # Find the message by ID
    message = Message.query.get(id)
    if message:
        # Update the message body
        message.body = new_body
        db.session.commit()
        return jsonify(message.serialize())
    else:
        return jsonify({'error': 'Message not found'}), 404

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    # Find the message by ID
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted'})
    else:
        return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
