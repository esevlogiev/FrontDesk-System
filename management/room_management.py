import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from create_database_tables import DATABASE_FILENAME
from classes.room import Room
from classes.convert_to_class_object import *
import create_database_tables

import datetime

def add_new_room(new_room, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('Select * from Rooms')
    rooms = cursor.fetchall()
    for room in rooms:
        if convert_room(room[0]).get_number == new_room.get_number:
            connection.close()
            return False
    cursor.execute("INSERT INTO Rooms(room) values (?)", (new_room,))      
    connection.commit()
    connection.close()
    return True

def release_room(room_number, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from Rooms")
    rooms = cursor.fetchall()
    len(rooms)
    for room in rooms:
        if int(convert_room(room[0]).get_number) == room_number and\
           convert_room(room[0]).is_rent == 'True':
            cursor.execute('''delete from Rooms where room = ?''', (room[0], ))
            update_room = convert_room(room[0])
            update_room.set_is_rent(False)
            cursor.execute("INSERT INTO Rooms(room) values (?)",
                           (update_room, ))
    connection.commit()
    connection.close()

def release_all_rooms(filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from Clients")
    clients = cursor.fetchall()
    for client in clients:
        date = convert_to_client(client[0]).get_date_registere
        stay = convert_to_client(client[0]).get_time_stay
        year, month, day = date.split("-")
        room_number = convert_to_client(client[0]).get_number_room
        if datetime.date(int(year), int(month), int(day)) +\
           datetime.timedelta(days=int(stay)) <= datetime.date.today():
            release_room(int(room_number), filename)
    connection.commit()
    connection.close()


def new_expire_date(old_manufacture_date, old_expire_date):
    year, month, day = old_manufacture_date.split("-")
    year_, month_, day_ = old_expire_date.split("-")
    expire_days = datetime.date(int(year_), int(month_), int(day_)) -\
                  datetime.date(int(year), int(month), int(day))
    return datetime.date.today() + datetime.timedelta(days=int(expire_days.days))


def change_food(filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from Food")
    foods = cursor.fetchall()
    for food in foods:
        if convert_to_food(food[0]).is_expire():
            new_food = convert_to_food(food[0])
            old_manufacture_date = convert_to_food(food[0]).get_manufacture_date
            old_expire_date = convert_to_food(food[0]).get_expire_date
                                                              
            new_food.replace(str(datetime.date.today()),
                             str(new_expire_date(old_manufacture_date,
                                 old_expire_date)))
            cursor.execute('''Delete from Food where food = ?''', (food[0],))
            cursor.execute('''Insert into Food(food) values (?)''', (new_food,))
    connection.commit()
    connection.close()


def change_bath_item(filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from BathItems")
    bath_items = cursor.fetchall()
    for bath_item in bath_items:
        if convert_bath_item(bath_item[0]).has_to_replace():
            new_bath_item = convert_bath_item(bath_item[0])
            new_bath_item.replace()
            cursor.execute('''delete from BathItems where bath_items = ?''',
                           (bath_item[0],))
            cursor.execute('''insert into BathItems(bath_items) values (?)''',
                           (new_bath_item,))
    connection.commit()
    connection.close()

def add_food(new_food, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Food(food) values (?)", (new_food,))
    connection.commit()
    connection.close()

def food_in_room(room_number, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from Food''')
    foods = cursor.fetchall()
    result = []
    for food in foods:
        if int(convert_to_food(food[0]).get_room_number) == room_number:
            result.append(convert_to_food(food[0]))
    connection.close()
    return result


def add_furniture(new_furniture, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Furniture(furniture) values (?)",
                   (new_furniture,))
    connection.commit()
    connection.close()

def furnitures_in_room(room_number, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from Furniture''')
    furnitures = cursor.fetchall()
    result = []
    for furniture in furnitures:
        if int(convert_to_furniture(furniture[0]).get_room_number) == room_number:
            result.append(convert_to_furniture(furniture[0]))
    connection.close()
    return result

def add_sleeping_furniture(new_sleeping_furniture, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO SleepingFurniture(sf) values (?)",
                   (new_sleeping_furniture,))
    connection.commit()
    connection.close()

def sleeping_furnitures_in_room(room_number, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from SleepingFurniture''')
    sleeping_furnitures = cursor.fetchall()
    result = []
    for sleeping_furniture in sleeping_furnitures:
        if int(convert_to_sleeping_furniture(
           sleeping_furniture[0]).get_room_number) == room_number:
            result.append(convert_to_sleeping_furniture(sleeping_furniture[0]))
    connection.close()
    return result

def add_bath_item(new_bath_item, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO BathItems(bath_items) values (?)",
                   (new_bath_item,))
    connection.commit()
    connection.close()

def bath_items_in_room(room_number, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from BathItems''')
    bath_items = cursor.fetchall()
    result = []
    for bath_item in bath_items:
        if int(convert_bath_item(bath_item[0]).get_room_number) == room_number:
            result.append(convert_bath_item(bath_item[0]))
    connection.close()
    return result

def get_all_free_rooms_number(filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from Rooms")
    rooms = cursor.fetchall()
    result = [convert_room(room[0]).get_number for room in rooms 
                if convert_room(room[0]).is_rent == "False"]
    connection.close()
    return result

def get_all_rooms_number(filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from Rooms")
    rooms = cursor.fetchall()
    result = [convert_room(room[0]).get_number for room in rooms]
    connection.close()
    return result


def get_room(room_number, filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("select * from Rooms")
    rooms = cursor.fetchall()
    for room in rooms:
        room_ = convert_room(room[0])
        if room_.get_number == room_number:
            return room_

def get_all_rooms(filename=DATABASE_FILENAME):
    return [get_room(room_number, filename) 
            for room_number in get_all_rooms_number(filename)]