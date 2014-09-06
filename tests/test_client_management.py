import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from create_database_tables import DATABASE_FILENAME
from classes.room import Room
from classes.convert_to_class_object import *
from create_database_tables import *
from management.room_management import *
from management.client_management import *
from management.reservation_management import *

from datetime import date, timedelta
from management.maid_management import add_maid

TEST_DATABASE_FILENAME = 'tests.db'

import unittest


class ClientManagementTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def setUp(self):
        create_tables(TEST_DATABASE_FILENAME)
        add_maid('Petyr', 'Mihailov', TEST_DATABASE_FILENAME)
        add_maid('Ivan', 'Kolev', TEST_DATABASE_FILENAME)
        add_maid('Nikola', 'Petrov', TEST_DATABASE_FILENAME)

    def add_test_rooms(self):
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'False')
        third_room = Room(102, 40, 10, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)
        add_new_room(third_room, TEST_DATABASE_FILENAME)

    def test_add_client(self):
        delete_clients_table_rows(TEST_DATABASE_FILENAME)
        delete_room_table_rows(TEST_DATABASE_FILENAME)
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'True')
        third_room = Room(102, 40, 10, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)
        add_new_room(third_room, TEST_DATABASE_FILENAME)

        client_first_day = date_to_string(date.today() + timedelta(days=2))
        new_client_first_day = date_to_string(date.today() + timedelta(days=4))
        client = Client('Roger', 'Federer', '0898671234', 100, 10,
                        client_first_day)
        other_client = Client('Rafael', 'Nadal', '0898671234', 101, 5,
                              new_client_first_day)

        self.assertTrue(add_client(client, 100, TEST_DATABASE_FILENAME))
        self.assertFalse(add_client(client, 101, TEST_DATABASE_FILENAME))
        self.assertTrue(add_client(client, 102, TEST_DATABASE_FILENAME))
        self.assertFalse(add_client(other_client, 100, TEST_DATABASE_FILENAME))
        self.assertFalse(add_client(other_client, 101, TEST_DATABASE_FILENAME))
        self.assertFalse(add_client(other_client, 102, TEST_DATABASE_FILENAME))

        release_room(101, TEST_DATABASE_FILENAME)
        self.assertTrue(add_client(other_client, 101, TEST_DATABASE_FILENAME))

        release_room(100, TEST_DATABASE_FILENAME)
        release_room(102, TEST_DATABASE_FILENAME)
        self.assertTrue(add_client(other_client, 100, TEST_DATABASE_FILENAME))
        self.assertTrue(add_client(other_client, 102, TEST_DATABASE_FILENAME))
        self.assertFalse(add_client(client, 101, TEST_DATABASE_FILENAME))

        release_room(101, TEST_DATABASE_FILENAME)
        self.assertTrue(add_client(other_client, 101, TEST_DATABASE_FILENAME))

    def test_show_client(self):
        delete_clients_table_rows(TEST_DATABASE_FILENAME)
        delete_room_table_rows(TEST_DATABASE_FILENAME)
        self.add_test_rooms()

        client_first_day = date_to_string(date.today() + timedelta(days=2))
        new_client_first_day = date_to_string(date.today() + timedelta(days=4))
        client = Client('Roger', 'Federer', '0898671234', 100, 10,
                        client_first_day)
        other_client = Client('Rafael', 'Nadal', '0898671234', 101, 5,
                              new_client_first_day)
        add_client(client, 100, TEST_DATABASE_FILENAME)

        client_first_day = date_to_string(date.today() + timedelta(days=30))
        client_ = Client('Roger', 'Federer', '0878956434', 102, 10,
                         client_first_day)
        add_client(client_, 102, TEST_DATABASE_FILENAME)
        add_client(other_client, 101, TEST_DATABASE_FILENAME)

        given_name_clients = [client[0]
                              for client in show_client('Roger', 'Federer',
                                                        TEST_DATABASE_FILENAME)]
        other_name_clients = [client[0]
                              for client in show_client('Rafael', 'Nadal',
                                                        TEST_DATABASE_FILENAME)]
        self.assertCountEqual([client, client_], given_name_clients)
        self.assertCountEqual([other_client], other_name_clients)
        self.assertNotEqual([client], given_name_clients)
        self.assertNotEqual([other_client, client], given_name_clients)
        self.assertFalse(show_client('Roger', 'Nadal', TEST_DATABASE_FILENAME))
        self.assertFalse(show_client('Rafael', 'Federer',
                                     TEST_DATABASE_FILENAME))

    def test_accomodate_clients(self):
        delete_room_table_rows(TEST_DATABASE_FILENAME)
        delete_clients_table_rows(TEST_DATABASE_FILENAME)
        delete_reservations_table_rows(TEST_DATABASE_FILENAME)
        self.add_test_rooms()

        date_registere = date_to_string(datetime.date.today())
        other_client_first_day = (date_to_string(date.today() +
                                  timedelta(days=4)))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        date_registere)
        other_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                              other_client_first_day)

        make_reservation(100, client, TEST_DATABASE_FILENAME)
        make_reservation(101, other_client, TEST_DATABASE_FILENAME)
        accomodate_clients(TEST_DATABASE_FILENAME)

        clients_with_maids = show_client('Roger', 'Federer',
                                         TEST_DATABASE_FILENAME)
        clients = [client[0] for client in clients_with_maids]
        self.assertTrue(client in clients)
        self.assertFalse(show_client('Rafael', 'Nadal',
                                     TEST_DATABASE_FILENAME))

    def test_get_client_id(self):
        delete_clients_table_rows(TEST_DATABASE_FILENAME)
        delete_room_table_rows(TEST_DATABASE_FILENAME)
        self.add_test_rooms()

        date_registere = date_to_string(datetime.date.today())
        other_client_first_day = (date_to_string(date.today() +
                                  timedelta(days=5)))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        date_registere)
        other_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                              other_client_first_day)
        add_client(client, 100, TEST_DATABASE_FILENAME)
        self.assertEqual(get_client_id(client, TEST_DATABASE_FILENAME), 0)
        add_client(other_client, 101, TEST_DATABASE_FILENAME)
        self.assertEqual(get_client_id(other_client, TEST_DATABASE_FILENAME),
                         1)
