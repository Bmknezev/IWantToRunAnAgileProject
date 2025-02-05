from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from pandas import DataFrame

import setup_database

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory storage for logged-in users and messages per room
logged_in = {
    'FID': [],
    'username': [],
    'password': [],
    'session': [],
}

# Message store, now supporting different rooms
messages = {}  # Dictionary where keys are room names and values are lists of messages


@socketio.on('connect')
def connect():
    print("connection made")
    emit('message', {'hello': "Hello"})


@socketio.on('login')
def login_handler(username, password):
    print("login called")
    print(username, password)
    FID = setup_database.find_user(username, password)
    if FID != setup_database.ERROR_CODE:
        logged_in['FID'].append(FID)
        logged_in['username'].append(username)
        logged_in['password'].append(password)
        logged_in['session'].append(request.remote_addr)
        return render_template("demo_page.html")
    else:
        print("Login Fail")
        return redirect("/chat")


@socketio.on('join_channel')
def handle_join_channel(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('receive_message', {'username': 'System', 'message': f'{username} has joined the room.'}, room=room)


# Leave a room (channel) event handler
@socketio.on('leave_channel')
def on_leave_channel(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit('message', {'message': f"{username} has left the room."}, room=room)


@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    emit('receive_message', {'username': username, 'message': message}, room=room)


@app.route('/chat')
def message_page_load():  # FID):
    if request.remote_addr in logged_in['session']:
        return render_template('demo_page.html')  # Render the chat page
    else:
        return "Login First to Access Chats"


@app.route('/')
def index():
    return render_template('demo_login.html')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)
