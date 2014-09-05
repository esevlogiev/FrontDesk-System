import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from create_database_tables import DATABASE_FILENAME
from classes.convert_to_class_object import *
import datetime
from management.room_management import get_all_free_rooms_number,\
                                       get_all_rooms_number
from management.client_management import date_to_string

def client_date_registere(client):
    date = client.get_date_registere
    year, month, day = date.split("-")
    return datetime.date(int(year), int(month), int(day))

def date_intersection(start_day, last_day, other_start_day, other_last_day):
    return (other_start_day >= start_day and other_start_day <= last_day or
            other_last_day >= start_day and other_last_day <= last_day or
            other_start_day <= start_day and other_last_day >= last_day)

def overbooking(client, new_client):
    client_stay = client.get_time_stay
    new_client_stay = new_client.get_time_stay

    client_first_day = client_date_registere(client)
    new_client_first_day = client_date_registere(new_client)
    client_last_day = client_first_day +\
                      datetime.timedelta(days=int(client_stay))
    new_client_last_day= new_client_first_day +\
                         datetime.timedelta(days=int(new_client_stay))

    return date_intersection(client_first_day, client_last_day,
                             new_client_first_day, new_client_last_day)

def make_reservation(room_number, new_client, filename = DATABASE_FILENAME):
    if client_date_registere(new_client) < datetime.date.today():
        return False
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select client from Reservations where room_number = ?''',
                   (room_number, ))
    current_room_clients = cursor.fetchall()
    overbooked = False
    for client in current_room_clients:
        if client_date_registere(convert_to_client(client[0])) <\
           datetime.date.today():
            continue
        if convert_to_client(client[0]).get_number_room == room_number and\
           overbooking(convert_to_client(client[0]), new_client):
            return False
    cursor.execute("INSERT INTO Reservations(room_number, client) values (?, ?)",\
                   (room_number, new_client))
    connection.commit()
    connection.close()
    return True


def cancel_reservation(room_number, first_name, last_name, date_registere,
                       filename = DATABASE_FILENAME):
    if (client_date_registere(Client('', '', '', 0, 0, date_registere)) <\
        datetime.date.today()):
        return False
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select client from Reservations where room_number = ?''',
                   (room_number, ))
    current_room_clients = cursor.fetchall()
    is_correct_reservation = False
    for client in current_room_clients:
        if convert_to_client(client[0]).get_first_name == first_name and \
           convert_to_client(client[0]).get_last_name == last_name and\
           convert_to_client(client[0]).get_date_registere == date_registere:
           cursor.execute('''delete from Reservations where client = ?''',
                          (client[0],))
           connection.commit()
           is_correct_reservation = True
    connection.close()
    return is_correct_reservation

def get_all_reservations(filename = DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Select * from Reservations''')
    reservations = cursor.fetchall()
    result = []
    for reservation in reservations:
        result.append(convert_to_client(reservation[1]))
    connection.close()
    return result
