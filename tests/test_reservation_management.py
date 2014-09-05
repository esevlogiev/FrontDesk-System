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

import datetime
from datetime import date, timedelta

TEST_DATABASE_FILENAME = 'tests.db'

import unittest

class ReservationsManagementTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args) 

    def setUp(self):
        create_tables(TEST_DATABASE_FILENAME)

    def test_overbooking(self):
        client_first_day = date_to_string(date.today() + timedelta(days=2))
        new_client_first_day = date_to_string(date.today() + timedelta(days=4))
        client = Client('Roger', 'Federer', '0898671234', 100, 10,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 5,
                            new_client_first_day)
        self.assertTrue(overbooking(client, new_client))

        client_first_day = date_to_string(date.today() + timedelta(days=5))
        new_client_first_day = date_to_string(date.today() + timedelta(days=14))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                            new_client_first_day)
        self.assertFalse(overbooking(client, new_client))

        client_first_day = date_to_string(date.today() + timedelta(days=3))
        new_client_first_day = date_to_string(date.today() + timedelta(days=6))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                            new_client_first_day)
        self.assertTrue(overbooking(client, new_client))
        
        client_first_day = date_to_string(date.today() + timedelta(days=4))
        new_client_first_day = date_to_string(date.today() + timedelta(days=2))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                            new_client_first_day)
        self.assertTrue(overbooking(client, new_client))

        client_first_day = date_to_string(date.today() + timedelta(days=4))
        new_client_first_day = date_to_string(date.today() + timedelta(days=2))
        client = Client('Roger', 'Federer', '0898671234', 100, 10,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 5,
                            new_client_first_day)
        self.assertTrue(overbooking(client, new_client))


        client_first_day = date_to_string(date.today() + timedelta(days=10))
        new_client_first_day = date_to_string(date.today() + timedelta(days=2))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 7,
                            new_client_first_day)
        self.assertFalse(overbooking(client, new_client))

    def test_make_reservation(self):
        delete_reservations_table_rows(TEST_DATABASE_FILENAME)
        delete_room_table_rows(TEST_DATABASE_FILENAME)
        delete_clients_table_rows(TEST_DATABASE_FILENAME)

        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)

        client_first_day = date_to_string(date.today() + timedelta(days=10))
        new_client_first_day = date_to_string(date.today() + timedelta(days=2))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        new_client = Client('Rafael', 'Nadal', '0898671234', 101, 7,
                            new_client_first_day)
        self.assertTrue(make_reservation(100, client, TEST_DATABASE_FILENAME))
        self.assertTrue(make_reservation(101, new_client, TEST_DATABASE_FILENAME))

        release_room(100, TEST_DATABASE_FILENAME)
        client_first_day = date_to_string(date.today() + timedelta(days=3))
        client = Client('Roger', 'Federer', '0898671234', 101, 5,
                        client_first_day)
        self.assertFalse(make_reservation(101, client, TEST_DATABASE_FILENAME))
        self.assertTrue(make_reservation(100, new_client, TEST_DATABASE_FILENAME))

    def test_cancel_reservation(self):
        delete_reservations_table_rows(TEST_DATABASE_FILENAME)
        delete_room_table_rows(TEST_DATABASE_FILENAME)
        delete_clients_table_rows(TEST_DATABASE_FILENAME)
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)

        client_first_day = date_to_string(date.today() + timedelta(days=10))
        new_client_first_day = date_to_string(date.today() + timedelta(days=2))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        other_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                              new_client_first_day)
        make_reservation(100, client, TEST_DATABASE_FILENAME)
        make_reservation(101, other_client, TEST_DATABASE_FILENAME)

        self.assertTrue(cancel_reservation(100, 'Roger', 'Federer',
                        client_first_day, TEST_DATABASE_FILENAME))
        self.assertFalse(cancel_reservation(100, 'Rogereeee', 'Federer',
                         client_first_day, TEST_DATABASE_FILENAME))
        self.assertTrue(cancel_reservation(101, 'Rafael', 'Nadal',
                        new_client_first_day, TEST_DATABASE_FILENAME))
        self.assertFalse(cancel_reservation(101, 'Rogereeee', 'Nadal',
                         client_first_day, TEST_DATABASE_FILENAME))
        self.assertFalse(cancel_reservation(100, 'Roger', 'Federer',
                         client_first_day, TEST_DATABASE_FILENAME))
        self.assertFalse(cancel_reservation(101, 'Rafael', 'Nadal',
                         new_client_first_day, TEST_DATABASE_FILENAME))

    def test_get_all_reservations(self):
        delete_reservations_table_rows(TEST_DATABASE_FILENAME)
        client_first_day = date_to_string(date.today() + timedelta(days=10))
        new_client_first_day = date_to_string(date.today() + timedelta(days=2))
        client = Client('Roger', 'Federer', '0898671234', 100, 5,
                        client_first_day)
        other_client = Client('Rafael', 'Nadal', '0898671234', 101, 10,
                              new_client_first_day)
        make_reservation(100, client, TEST_DATABASE_FILENAME)
        make_reservation(101, other_client, TEST_DATABASE_FILENAME)
        self.assertCountEqual(get_all_reservations(TEST_DATABASE_FILENAME), 
                              [client, other_client])
        self.assertNotEqual(get_all_reservations(TEST_DATABASE_FILENAME),
                            [client])
        self.assertNotEqual(get_all_reservations(TEST_DATABASE_FILENAME),
                            [other_client])
        self.assertNotEqual(get_all_reservations(TEST_DATABASE_FILENAME), [])
        self.assertTrue(client in get_all_reservations(TEST_DATABASE_FILENAME))
        self.assertTrue(other_client in get_all_reservations(TEST_DATABASE_FILENAME))
