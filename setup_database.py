import sqlite3

import sqlite3

#con = sqlite3.connect("test.db")
#cursor = con.cursor()
#cursor.execute("CREATE TABLE User (username CHAR(200), password CHAR(200), id CHAR(30))")
#cursor.execute("CREATE TABLE ChatHistory ( FID_1 CHAR(30), FID_2 CHAR(30), message CHAR(500), msgOrder INT, fromWho CHAR(30) )")

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

def insert_chat(FID_A, FID_B, message, fromWho):

    fid_1, fid_2 = id_order(FID_A, FID_B)

    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    order = cursor.execute(f"select count(*) from ChatHistory where FID_1 = '{fid_1}' and FID_2 = '{fid_2}'").fetchall()[0][0]
    order = order + 1
    #print(order)

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

    user_admin = "Said"
    user_b = "Barry"
    user_c = "Claire"
    user_d = "Dorothy"

    password_universal = "123"

    create_user(user_admin, password_universal, FID_A)
    create_user(user_b, password_universal, FID_B)
    create_user(user_c, password_universal, FID_C)
    create_user(user_d, password_universal, FID_D)

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

    print( find_chats(FID_A, FID_B) )
    print( find_chats(FID_A, FID_C) )
    print( find_chats(FID_A, FID_D) )

    print( find_chats(FID_C, FID_D) )

#sql_del = cursor.execute("DELETE FROM User")
#sql_del2 = cursor.execute("DELETE FROM ChatHistory")
#print("Total users affected: ", sql_del.rowcount)
#print("Total chats affected: ", sql_del2.rowcount)
#con.commit()

#populate_users()

def diagnostics():
    con = sqlite3.connect("test.db")
    cursor = con.cursor()

    print( find_chats( "0US8P7", "A30C7H") )
    print( cursor.execute("select * from User").fetchall() )
    print( cursor.execute("select * from ChatHistory").fetchall() )

diagnostics()