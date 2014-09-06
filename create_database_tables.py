import sqlite3

DATABASE_FILENAME = 'front_desk_system.db'


def create_tables(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Create table if not exists Rooms(room)''')
    cursor.execute('''Create table if not exists Food (food)''')
    cursor.execute('''Create table if not exists Furniture (furniture)''')
    cursor.execute('''Create table if not exists BathItems (bath_items)''')
    cursor.execute('''Create table if not exists SleepingFurniture (sf)''')
    cursor.execute('''Create table if not exists Clients(client)''')
    cursor.execute('''Create table if not exists Maids(first_name, last_name,\
                   client_id)''')
    cursor.execute('''Create table if not exists Reservations(room_number,\
                   client)''')
    connection.close()


def delete_clients_table_rows(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Delete from Clients''')
    connection.commit()
    connection.close()


def delete_room_table_rows(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Delete from Rooms''')
    connection.commit()
    connection.close()


def delete_reservations_table_rows(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Delete from Reservations''')
    connection.commit()
    connection.close()


def delete_maids_table_rows(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''Delete from Maids''')
    connection.commit()
    connection.close()
