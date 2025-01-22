from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, send
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # To store sessions on the filesystem
Session(app)
socketio = SocketIO(app, manage_session=False)  # Disable socket session management

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('username.html')  # A new template for setting username

@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.form.get('username')
    if username:
        session['username'] = username
        return redirect(url_for('chat'))
    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', username=session['username'])

@socketio.on('message')
def handle_message(msg):
    if 'username' in session:
        username = session['username']
        send(f"{username}: {msg}", broadcast=True)
    else:
        send("Unauthorized message", broadcast=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)
