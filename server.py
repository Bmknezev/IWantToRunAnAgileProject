from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit,send
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

isUpdated = {

}

# now you can access the FID based on the IP address of somebody
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

@socketio.on('new_account')
def new_account(username, password):
    print("new account")
    setup_database.create_user(username, password)

    FID = setup_database.find_user(username, password)

    logged_in['FID'].append(FID)
    logged_in['username'].append(username)
    logged_in['password'].append(password)
    logged_in['session'].append(request.remote_addr)

    isUpdated[FID] = {"isUpdated": 0, "fromWho": "", "fromID": "", "message": ""}

    return f"account made \n Username: {username} \n Password: {password}"

@socketio.on('logout')
def logout_handler():
    print("logout called")
    index = get_index_by_IP(request.remote_addr)
    logged_in['FID'].pop(index)
    logged_in['username'].pop(index)
    logged_in['password'].pop(index)
    logged_in['session'].pop(index)

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
        isUpdated[FID] = {"isUpdated": 0, "fromWho": "", "fromID": "", "message": ""}
        #return redirect(url_for('message_page_load', FID=FID))
        emit('login_success', "/chat")
        return
    else:
        print("Login Fail")
        emit('login_fail', "Login Failed")
        return


@app.route('/chat')
def message_page_load():#FID):
    print("accessing msgs")
    #if FID in logged_in['FID'] and request.remote_addr in logged_in['session']:
    if request.remote_addr in logged_in['session']:
        return render_template('demo_page.html')
    else:
        return "Login First to Access Chats"


@socketio.on('connecting_need_friends')
def give_page_friend_list():
    ip = request.remote_addr
    FID = get_FID_by_IP(ip)
    print(f"connecting friends for {FID}")
    friends = setup_database.get_friends(FID)

    return friends

@socketio.on('send_message')
def store_msg(room_ID, msg):
    FID = setup_database.get_FID_by_name(room_ID)
    sender_FID = get_FID_by_IP(request.remote_addr)

    print("msg recieved: " + str(msg) )
    print("room ID: " + str(room_ID))
    print("FID: " + str(FID))
    print("sender FID: " + str(sender_FID))

    if FID in logged_in['FID']:
        isUpdated[FID]["isUpdated"] = 1
        isUpdated[FID]["fromWho"].append(setup_database.get_name_by_FID(get_FID_by_IP(request.remote_addr)))
        isUpdated[FID]["fromID"].append( get_FID_by_IP(request.remote_addr))
        isUpdated[FID]["message"].append(msg)

    sender_name = setup_database.get_name_by_FID(str(sender_FID))
    print("sender name: " + str(sender_name))
    setup_database.insert_chat(FID, sender_FID, msg, sender_FID)
    response = [sender_name, msg]
    emit('receive_message', response, to=sender_name)

    return response

@socketio.on('ask_for_update')
def refresh():
    print("test refresh: ", isUpdated[get_FID_by_IP(request.remote_addr)])
    check = isUpdated[get_FID_by_IP(request.remote_addr)]["isUpdated"]
    name = isUpdated[get_FID_by_IP(request.remote_addr)]["fromWho"]
    id = isUpdated[get_FID_by_IP(request.remote_addr)]["fromID"]
    message = isUpdated[get_FID_by_IP(request.remote_addr)]["message"]

    isUpdated[get_FID_by_IP(request.remote_addr)]["isUpdated"] = 0
    isUpdated[get_FID_by_IP(request.remote_addr)]["fromWho"] = []
    isUpdated[get_FID_by_IP(request.remote_addr)]["fromID"] = []
    isUpdated[get_FID_by_IP(request.remote_addr)]["message"] = []
    return check, name, id, message

@socketio.on('in_channel_get_msgs')
def give_msgs(room_ID):
    FID_A = get_FID_by_IP(request.remote_addr)
    FID_B = setup_database.get_FID_by_name(room_ID)
    chats = setup_database.find_chats( FID_A, FID_B )
    chats_new = [[None for k in range(5)] for i in range(len(chats))]

    for c in range(len(chats)):
        print(chats[c])
        chats_new[c][0] = setup_database.get_name_by_FID(chats[c][0])
        chats_new[c][1] = setup_database.get_name_by_FID(chats[c][1])
        chats_new[c][2] = chats[c][2]
        chats_new[c][3] = chats[c][3]
        chats_new[c][4] = setup_database.get_name_by_FID(chats[c][4])
        print(chats_new[c])

    isUpdated[FID_A]["isUpdated"] = 0
    return chats_new

@socketio.on('add_new_friend')
def add_friend_to_list(FID_to_add):
    FID_A = get_FID_by_IP(request.remote_addr)

    #isFriendExist = ''
    try:
        isFriendExist = setup_database.get_name_by_FID(FID_to_add)
    except IndexError:
        return -1

    if isFriendExist:
        friend_names = setup_database.get_friends(FID_A)
        friend_IDs = []
        for friend_name in friend_names:
            friend_IDs.append(setup_database.get_FID_by_name(friend_name) )
        if FID_to_add in friend_IDs:
            return -2
        setup_database.add_friend(FID_A, FID_to_add)
        return isFriendExist
    else:
        return -1

@socketio.on('show_FID')
def show_FID():
    fid = get_FID_by_IP(request.remote_addr)
    print(fid)
    return fid

@socketio.on('notification')
def notify_user(msg):
    print("notification: " + msg)
    return

@socketio.on('test')
def test():
    print("here")
    return





@app.route('/')
def index():
    return render_template('demo_login.html')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)
