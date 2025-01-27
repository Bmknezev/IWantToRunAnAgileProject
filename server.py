from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from pandas import DataFrame

import setup_database
app = Flask(__name__)
socketio = SocketIO(app)

logged_in = {
    'FID': [],
    'username': [],
    'password': [],
    'session': [],
}

# now you can access the FID based on the IP address of someboy
# get_FID_by_IP(request.remote_addr) # this is the fastest way to use it in any socketio function
def get_FID_by_IP(ip):
    loc_in_logged = logged_in['session'].index(ip)
    return logged_in['FID'][loc_in_logged]

# need more info? get the specific index you need from the logger
def get_index_by_IP(ip):
    return logged_in['session'].index(ip)

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
        print( setup_database.find_user(username, password) )
        logged_in['FID'].append(FID)
        logged_in['username'].append(username)
        logged_in['password'].append(password)
        logged_in['session'].append(request.remote_addr)
        #return redirect(url_for('message_page_load', FID=FID))
        return render_template("demo_page.html")
    else:
        print("Login Fail")
        return redirect("/chat")


@app.route('/chat')
def message_page_load():#FID):
    print("accessing msgs")
    #if FID in logged_in['FID'] and request.remote_addr in logged_in['session']:
    if request.remote_addr in logged_in['session']:
        return render_template('demo_page.html')
    else:
        return "Login First to Access Chats"


@app.route('/')
def index():
    return render_template('demo_login.html')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)
