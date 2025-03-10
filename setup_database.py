import sqlite3

import sqlite3

#con = sqlite3.connect("test.db")
#cursor = con.cursor()
#cursor.execute("CREATE TABLE User (username CHAR(200), password CHAR(200), id CHAR(30))")
#cursor.execute("CREATE TABLE ChatHistory ( FID_1 CHAR(30), FID_2 CHAR(30), message CHAR(500), msgOrder INT, fromWho CHAR(30) )")
#cursor.execute("CREATE TABLE Friends ( FID_1 CHAR(30), FID_2 CHAR(30) )")


import string
import random

ERROR_CODE = "-1"

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def id_order(FID_A, FID_B):
    fid_1 = ""
    fid_2 = ""
    if FID_A < FID_B:
        fid_1 = FID_A
        fid_2 = FID_B
    else:
        fid_1 = FID_B
        fid_2 = FID_A
    return fid_1, fid_2

def add_friend(FID_A, FID_B):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    new_friend_A_cmd = f"INSERT INTO FRIENDS VALUES ('{FID_A}', '{FID_B}')"
    new_friend_B_cmd = f"INSERT INTO FRIENDS VALUES ('{FID_B}', '{FID_A}')"

    cursor.execute(new_friend_A_cmd)
    cursor.execute(new_friend_B_cmd)

    con.commit()

def get_name_by_FID(FID):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    if isinstance(FID, tuple):
        FID = FID[0]

    name = cursor.execute("SELECT DISTINCT username FROM User WHERE id = ?", (FID,) ).fetchall()[0][0]

    return name

def get_FID_by_name(name):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()
    FID = cursor.execute(f"SELECT DISTINCT id FROM User WHERE username = '{name}'").fetchall()[0][0]#, (name)).fetchall()

    return FID

def get_friends(FID):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    get_frd_cmd = f"SELECT FID_2 FROM FRIENDS WHERE FID_1 = '{FID}'"
    friends = cursor.execute(get_frd_cmd).fetchall()
    friend_names = []

    for friend in friends:
        friend_names.append( get_name_by_FID(friend) )

    return friend_names

def insert_chat(FID_A, FID_B, message, fromWho):

    fid_1, fid_2 = id_order(FID_A, FID_B)

    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    order = cursor.execute(f"select count(*) from ChatHistory where FID_1 = '{fid_1}' and FID_2 = '{fid_2}'").fetchall()[0][0]
    order = order + 1
    print(f"msg order: {order}")

    cursor.execute("""
                   INSERT INTO ChatHistory (FID_1, FID_2, message, msgOrder, fromWho) 
                   VALUES ('{fid_1}', '{fid_2}', '{message}', {order}, '{fromWho}')
                   """.format(fid_1=fid_1, fid_2=fid_2, message=message, order=order, fromWho=fromWho) )

    #cursor.execute("INSERT INTO User VALUES ('test', 567, 2)")
    #print( cursor.execute("select username from User").fetchall() )
    #print( cursor.execute("select * from ChatHistory").fetchall() )

    con.commit()

def find_chats(FID_A, FID_B):
    fid_1, fid_2 = id_order(FID_A, FID_B)

    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    chats = cursor.execute( f"select * from ChatHistory where FID_1 == '{fid_1}' and FID_2 == '{fid_2}' order by msgOrder" ).fetchall()
    #print(chats)
    return chats

def create_user(username, password, FID=id_generator()):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    isPrevUser = cursor.execute(f"""select count(*) from User 
                                    where username = '{username}'
                                    """).fetchall()[0][0]
    if isPrevUser == 0:
        cursor.execute(f"INSERT INTO User VALUES ('{username}', '{password}', '{FID}')" )
    con.commit()
def find_user(username, password):
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    try:
        FID = cursor.execute( f"""select id from User 
                             where username = '{username}' 
                             and password = '{password}'""" ).fetchall()[0][0]
        print(FID)
        return FID
    except IndexError:
        return ERROR_CODE

def populate_users():
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    FID_A = id_generator()
    FID_B = id_generator()
    FID_C = id_generator()
    FID_D = id_generator()
    FID_F = id_generator()

    user_admin = "Said"
    user_b = "Barry"
    user_c = "Claire"
    user_d = "Dorothy"
    user_to_add_as_friend = "Francois"

    password_universal = "123"

    create_user(user_admin, password_universal, FID_A)
    create_user(user_b, password_universal, FID_B)
    create_user(user_c, password_universal, FID_C)
    create_user(user_d, password_universal, FID_D)
    create_user(user_to_add_as_friend, password_universal, FID_F)

    print(cursor.execute("select * from User").fetchall())

    message_1 = "hi"
    message_2 = "hello"
    message_3 = "good morning"
    message_4 = "good afternoon"
    message_5 = "you good?"
    message_6 = "yeah i am"

    insert_chat(FID_A, FID_B, message_1, FID_A)
    insert_chat(FID_A, FID_B, message_2, FID_B)

    insert_chat(FID_A, FID_C, message_3, FID_A)
    insert_chat(FID_A, FID_C, message_4, FID_C)

    insert_chat(FID_A, FID_D, message_5, FID_A)
    insert_chat(FID_A, FID_D, message_6, FID_D)

    add_friend(FID_A, FID_B)
    add_friend(FID_A, FID_C)
    add_friend(FID_A, FID_D)

    print( find_chats(FID_A, FID_B) )
    print( find_chats(FID_A, FID_C) )
    print( find_chats(FID_A, FID_D) )

    print( find_chats(FID_C, FID_D) )


def wipeout():
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    sql_del = cursor.execute("DELETE FROM User")
    sql_del2 = cursor.execute("DELETE FROM ChatHistory")
    print("Total users affected: ", sql_del.rowcount)
    print("Total chats affected: ", sql_del2.rowcount)
    con.commit()



def diagnostics():
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
    print("Tables: ",  cursor.execute(sql_query).fetchall() )

    print("Users: ", cursor.execute("select * from User").fetchall() )
    print("All Chats: ",  cursor.execute("select * from ChatHistory").fetchall() )
    print("Said's Friends: ", get_friends(get_FID_by_name("Said")))
    print("\nSaid and Barry's DMs")
    print(find_chats(get_FID_by_name("Said"), get_FID_by_name("Barry")))



#wipeout()
#populate_users()

diagnostics()

