from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    room = request.args.get('room')
    username = request.args.get('username')
    if room and username:
        return render_template('index.html', room=room, username=username)
    else:
        return "Error: please provide a room and a username."

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    message = username + ' has entered the room.'
    emit('message', {'username': 'System', 'message': message}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    message = username + ' has left the room.'
    emit('message', {'username': 'System', 'message': message}, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    emit('message', {'username': username, 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)



# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# # Endpoint for receiving messages
# @app.route('/message', methods=['POST'])
# def message():
#     message = request.form.get('message')
#     # Process message and send back response
#     response = 'You said: ' + message
#     return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(debug=True)
