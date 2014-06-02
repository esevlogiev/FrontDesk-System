import sqlite3
from room import Room
from Food import Food
from SleepingFurniture import Furniture
import os
from convert_to_class_object import *

db_filename = 'todo.db'

db_is_new = not os.path.exists(db_filename)

conn = sqlite3.connect(db_filename)

if db_is_new:
    print('Need to create schema')
else:
    print('Database exists, assume schema does, too.')

conn.close()


def add_new_room(try_room, items):
    db = sqlite3.connect(db_filename)
    cursor = db.cursor()
    cursor.execute("select * from ROOMS")
    rooms = cursor.fetchall()
    counter = 0
    for room in rooms:
        if int(convert_room(room[0]).number) == try_room.number:
            print("The room exists!!!")
            break
        counter += 1
    if counter == len(rooms):
        cursor.execute("INSERT INTO ROOMS(r) values (?)", (try_room,))
        cursor.execute("create table '%s' (item items)" % str(try_room.number))
        for item in items:
            cursor.execute("INSERT INTO '%s' values (?)" % str(try_room.number), (item,))
    cursor.execute("select * from '%s'" % str(try_room.number))    
    db.commit()
    db.close()   
