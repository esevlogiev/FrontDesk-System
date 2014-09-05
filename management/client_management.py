import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from create_database_tables import DATABASE_FILENAME
from classes.convert_to_class_object import *
from datetime import date
import datetime
from classes.client import Client
from management.room_management import get_room
from management.maid_management import (add_maid_to_serve_client,
                                        get_maid_names, get_the_least_busy_maid,
                                        set_maid_to_client)



def get_client_id(client, filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from Clients''')
    clients = [convert_to_client(client[0]) for client in cursor.fetchall()]
    #return clients.index(client)
    index = 0
    for database_client in clients:
        if database_client == client:
            return index
        index += 1
    return False

def add_client(client, room_number, filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    room = get_room(room_number, filename)
    if  room.get_is_rent == 'False':
        update_room = Room(room.get_number, room.get_price_per_day, 
                           room.get_capacity, "True")
        cursor.execute("UPDATE Rooms set room = ? WHERE room = ?", (update_room,
                                                                    room))
        cursor.execute("INSERT INTO Clients(client) values (?)", (client,))
        connection.commit()
        connection.close()
        client_id = get_client_id(client, filename)
        set_maid_to_client(client_id, filename)
        return True
    return False

def date_to_string(date):
    if type(date) == datetime.date:
        year, month, day = str(date.year), str(date.month), str(date.day)
    else:
        year, month, day = str(date.year()), str(date.month()), str(date.day())
    return year + '-' + month + '-' + day

def show_client(first_name, last_name, filename=DATABASE_FILENAME):
    is_client = False
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("Select * from Clients")
    clients = cursor.fetchall()
    result = []
    for client in clients:
        client_ = convert_to_client(client[0])
        if (client_.get_first_name == first_name and
            client_.get_last_name == last_name):
            client_id = get_client_id(client_, filename)
            maid_names = get_maid_names(client_id, filename)
            result.append((client_, maid_names))
    connection.close()
    if result == []:
        return False
    return result

def show_all_clients(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("Select * from Clients")
    clients = cursor.fetchall()
    if clients == []:
        return False
    return clients

def accomodate_clients(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from Reservations ''')
    reservations = cursor.fetchall()
    new_clients = []
    for reservation in reservations:
        if (convert_to_client(reservation[1]).get_date_registere ==
            date_to_string(date.today())):
            new_clients.append(convert_to_client(reservation[1]))
    for client in new_clients:
        add_client(client, client.get_number_room, filename)
    connection.close()

def get_all_clients(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from Clients ''')
    return [convert_to_client(client[0]) for client in cursor.fetchall()]