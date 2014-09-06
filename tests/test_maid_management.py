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

from management.maid_management import *


class MaidsManagementTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def setUp(self):
        create_tables(TEST_DATABASE_FILENAME)

    def test_add_maid(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid('Petyr', 'Ivanov', TEST_DATABASE_FILENAME)
        add_maid('Kiril', 'Georgiev', TEST_DATABASE_FILENAME)
        add_maid('Nikola', 'Todorov', TEST_DATABASE_FILENAME)
        maids = get_all_maids(TEST_DATABASE_FILENAME)
        self.assertCountEqual(maids, [('Petyr', 'Ivanov'),
                                      ('Kiril', 'Georgiev'),
                                      ('Nikola', 'Todorov')])
        self.assertNotEqual(maids, [('Petyr', 'Ivanov'),
                                    ('Kiril', 'Georgiev')])
        self.assertTrue(('Petyr', 'Ivanov') in maids)
        self.assertTrue(('Kiril', 'Georgiev') in maids)
        self.assertTrue(('Nikola', 'Todorov') in maids)
        self.assertFalse(('Nikola', 'Petrov') in maids)

    def test_add_maid_to_serve_client(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Petyr', 'Ivanov', 1,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 2,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Nikola', 'Todorov', 3,
                                 TEST_DATABASE_FILENAME)
        maids = get_all_maids(TEST_DATABASE_FILENAME)
        self.assertCountEqual(maids, [('Petyr', 'Ivanov'),
                                      ('Kiril', 'Georgiev'),
                                      ('Nikola', 'Todorov')])
        self.assertTrue(('Petyr', 'Ivanov') in maids)
        self.assertTrue(('Kiril', 'Georgiev') in maids)
        self.assertTrue(('Nikola', 'Todorov') in maids)
        self.assertFalse(('Nikola', 'Petrov') in maids)

    def test_get_all_maids_names(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid('Petyr', 'Ivanov', TEST_DATABASE_FILENAME)
        add_maid('Kiril', 'Georgiev', TEST_DATABASE_FILENAME)
        add_maid('Nikola', 'Todorov', TEST_DATABASE_FILENAME)
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from Maids''')
        maids = cursor.fetchall()
        cursor.close()
        self.assertCountEqual(maids, [('Petyr', 'Ivanov', -1),
                                      ('Kiril', 'Georgiev', -1),
                                      ('Nikola', 'Todorov', -1)])
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Petyr', 'Ivanov', 1,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 2,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Nikola', 'Todorov', 3,
                                 TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from Maids''')
        maids = cursor.fetchall()
        self.assertCountEqual(maids, [('Petyr', 'Ivanov', 1),
                                      ('Kiril', 'Georgiev', 2),
                                      ('Nikola', 'Todorov', 3)])

    def test_choose_maid(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Petyr', 'Ivanov', 1,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 2,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Nikola', 'Todorov', 3,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 4,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Nikola', 'Todorov', 5,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 6,
                                 TEST_DATABASE_FILENAME)
        maid = get_the_least_busy_maid(TEST_DATABASE_FILENAME)
        self.assertEqual((maid[0], maid[1]), ('Petyr', 'Ivanov'))
        self.assertNotEqual((maid[0], maid[1]), ('Nikola', 'Georgiev'))
        self.assertNotEqual((maid[0], maid[1]), ('Nikola', 'Todorov'))

    def test_get_maid_names(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Petyr', 'Ivanov', 1,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 2,
                                 TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Nikola', 'Todorov', 3,
                                 TEST_DATABASE_FILENAME)
        self.assertEqual('Petyr Ivanov', get_maid_names(1,
                         TEST_DATABASE_FILENAME))
        self.assertEqual('Kiril Georgiev', get_maid_names(2,
                         TEST_DATABASE_FILENAME))
        self.assertEqual('Nikola Todorov', get_maid_names(3,
                         TEST_DATABASE_FILENAME))
        self.assertNotEqual('Petyr Ivanov', get_maid_names(3,
                            TEST_DATABASE_FILENAME))
        self.assertNotEqual('Kiril Georgiev', get_maid_names(1,
                            TEST_DATABASE_FILENAME))
        self.assertNotEqual('Nikola Todorov', get_maid_names(2,
                            TEST_DATABASE_FILENAME))

    def test_set_maid_to_client(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid('Petyr', 'Ivanov', TEST_DATABASE_FILENAME)
        set_maid_to_client(3, TEST_DATABASE_FILENAME)
        self.assertTrue(('Petyr', 'Ivanov', 3) in
                        get_all_maid_characteristics(TEST_DATABASE_FILENAME))
        add_maid('Kiril', 'Ivanov', TEST_DATABASE_FILENAME)
        set_maid_to_client(4, TEST_DATABASE_FILENAME)
        self.assertTrue(('Kiril', 'Ivanov', 4) in
                        get_all_maid_characteristics(TEST_DATABASE_FILENAME))

    def test_get_all_maids_characteristics(self):
        delete_maids_table_rows(TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Petyr', 'Ivanov', 1, TEST_DATABASE_FILENAME)
        add_maid_to_serve_client('Kiril', 'Georgiev', 2,
                                 TEST_DATABASE_FILENAME)
        maids = get_all_maid_characteristics(TEST_DATABASE_FILENAME)
        self.assertCountEqual([('Petyr', 'Ivanov', 1),
                               ('Kiril', 'Georgiev', 2)], maids)
