import sqlite3

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from create_database_tables import DATABASE_FILENAME
import create_database_tables

import collections


def add_maid(first_name, last_name, filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Maids(first_name, last_name, client_id) values\
                    (?, ?, ?)", (first_name, last_name, -1))
    connection.commit()
    connection.close()
    return True


def add_maid_to_serve_client(first_name, last_name,
                             client_id, filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Maids(first_name, last_name, client_id) values\
                    (?, ?, ?)", (first_name, last_name, client_id))
    connection.commit()
    connection.close()


def get_all_maids(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("Select * from Maids")
    all_maids = [(maid[0], maid[1]) for maid in cursor.fetchall()]
    unique_maids = list(set(all_maids))
    connection.close()
    return unique_maids


def get_the_least_busy_maid(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("Select * from Maids")
    maids = cursor.fetchall()
    if maids == []:
        return
    maids = [(maid[0], maid[1]) for maid in maids]
    counter = collections.Counter(maids)
    unique_maids_len = len(get_all_maids(filename))
    return counter.most_common()[unique_maids_len - 1][0]


def get_maid_names(maid_id, filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("Select * from Maids where client_id = ?", (maid_id,))
    maid = cursor.fetchone()
    if maid is None:
        return
    return maid[0] + ' ' + maid[1]


def set_maid_to_client(client_id, filename=DATABASE_FILENAME):
    maid = get_the_least_busy_maid(filename)
    add_maid_to_serve_client(maid[0], maid[1], client_id, filename)


def get_all_maid_characteristics(filename=DATABASE_FILENAME):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("Select * from Maids")
    maids = cursor.fetchall()
    cursor.close()
    return maids
