import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from create_database_tables import DATABASE_FILENAME
from classes.room import Room
from classes.convert_to_class_object import *
from create_database_tables import create_tables
from management.room_management import *
from management.client_management import *

from datetime import date, timedelta

TEST_DATABASE_FILENAME = 'tests.db'

import unittest


class RoomManagementTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def setUp(self):
        create_tables(TEST_DATABASE_FILENAME)

    def delete_room_table_rows(self):
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Delete from Rooms''')
        connection.commit()
        connection.close()

    def delete_clients_table_rows(self):
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Delete from Clients''')
        connection.commit()
        connection.close()

    def delete_bath_items_table_rows(self):
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Delete from BathItems''')
        connection.commit()
        connection.close()

    def delete_food_table_rows(self):
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Delete from Food''')
        connection.commit()
        connection.close()

    def delete_furniture_table_rows(self):
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Delete from Furniture''')
        connection.commit()
        connection.close()

    def delete_sleeping_furniture_table_rows(self):
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Delete from SleepingFurniture''')
        connection.commit()
        connection.close()

    def test_add_new_room(self):
        self.delete_room_table_rows()
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'False')
        third_room = Room(102, 40, 10, 'False')
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from Rooms''')
        cursor.execute("INSERT INTO Rooms(room) values (?)", (first_room, ))
        cursor.execute("INSERT INTO Rooms(room) values (?)", (second_room, ))
        cursor.execute("INSERT INTO Rooms(room) values (?)", (third_room, ))
        connection.commit()
        connection.close()

        self.assertTrue(add_new_room(Room(103, 5, 5, 'False'),
                        TEST_DATABASE_FILENAME), 'room can not be add')
        self.assertFalse(add_new_room(first_room, TEST_DATABASE_FILENAME),
                         'room can not be add')
        self.assertFalse(add_new_room(Room(100, 10, 10, 'False'),
                         TEST_DATABASE_FILENAME), 'room can not be add')
        self.assertTrue(add_new_room(Room(104, 5, 5, 'False'),
                        TEST_DATABASE_FILENAME), 'room can not be add')
        self.assertFalse(add_new_room(second_room, TEST_DATABASE_FILENAME),
                         'room can not be add')
        self.assertFalse(add_new_room(Room(101, 10, 10, 'False'),
                         TEST_DATABASE_FILENAME), 'room can not be add')
        self.assertTrue(add_new_room(Room(105, 5, 5, 'False'),
                        TEST_DATABASE_FILENAME), 'room can not be add')
        self.assertFalse(add_new_room(third_room, TEST_DATABASE_FILENAME),
                         'room can not be add')
        self.assertFalse(add_new_room(Room(102, 10, 10, 'False'),
                         TEST_DATABASE_FILENAME), 'room can not be add')

    def test_added_rooms(self):
        self.delete_room_table_rows()
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'False')
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Rooms(room) values (?)", (first_room, ))
        cursor.execute("INSERT INTO Rooms(room) values (?)", (second_room, ))
        connection.commit()
        rooms = [second_room, first_room]
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from Rooms''')
        add_rooms = cursor.fetchall()
        self.assertCountEqual([convert_room(room[0]) for room in add_rooms],
                              rooms)
        connection.close()

    def test_release_room(self):
        self.delete_room_table_rows()
        first_room = Room(100, 20, 5, 'True')
        second_room = Room(101, 30, 6, 'True')
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Rooms(room) values (?)", (first_room, ))
        cursor.execute("INSERT INTO Rooms(room) values (?)", (second_room, ))
        connection.commit()
        connection.close()

        room = get_room(100, TEST_DATABASE_FILENAME)
        self.assertEqual('True', room.is_rent)
        self.assertNotEqual('False', room.is_rent)

        release_room(100, TEST_DATABASE_FILENAME)
        room = get_room(100, TEST_DATABASE_FILENAME)
        self.assertEqual('False', room.is_rent)
        self.assertNotEqual('True', room.is_rent)

    def test_release_all_rooms(self):
        self.delete_clients_table_rows()
        self.delete_room_table_rows()
        add_new_room(Room(120, 20, 5, 'False'), TEST_DATABASE_FILENAME)
        add_new_room(Room(121, 30, 6, 'False'), TEST_DATABASE_FILENAME)
        client = Client('Roger', 'Federer', '0898671234', 120, 5, '2014-08-20')
        other_client = Client('Rafael', 'Nadal', '0898671234', 121, 10,
                              '2014-08-16')

        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        add_client(client, 120, TEST_DATABASE_FILENAME)
        add_client(other_client, 121, TEST_DATABASE_FILENAME)
        release_all_rooms(TEST_DATABASE_FILENAME)

        cursor.execute('''Select * from Rooms''')
        rooms_rent = [convert_room(room[0]).is_rent
                      for room in cursor.fetchall()]
        self.assertTrue(all(room_rent == 'False' for room_rent in rooms_rent))
        self.assertFalse(any(room_rent == 'True' for room_rent in rooms_rent))
        connection.close()

    def test_getting_room_bath_items(self):
        self.delete_bath_items_table_rows()
        bath_item = BathItems('tooth brush', "2014-10-10", 20, 120)
        other_bath_item = BathItems('shampoo', "2014-9-10", 20, 121)
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO BathItems(bath_items) values (?)",
                       (bath_item, ))
        cursor.execute("INSERT INTO BathItems(bath_items) values (?)",
                       (other_bath_item, ))
        connection.commit()

        room_bath_items = bath_items_in_room(120, TEST_DATABASE_FILENAME)
        self.assertCountEqual([bath_item], room_bath_items)
        self.assertNotEqual([bath_item, other_bath_item], room_bath_items)

        other_room_bath_items = bath_items_in_room(121, TEST_DATABASE_FILENAME)
        self.assertCountEqual([other_bath_item], other_room_bath_items)
        self.assertNotEqual([bath_item, other_bath_item],
                            other_room_bath_items)

        connection.close()

    def test_getting_room_food(self):
        self.delete_food_table_rows()
        food = Food('eggs', 5, '2014-8-10', '2014-9-10', 120)
        other_food = Food('meat', 2, '2014-8-20', '2014-8-27', 121)

        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Food(food) values (?)", (food, ))
        cursor.execute("INSERT INTO Food(food) values (?)", (other_food, ))
        connection.commit()

        room_food = food_in_room(120, TEST_DATABASE_FILENAME)
        self.assertCountEqual([food], room_food)
        self.assertNotEqual([food, other_food], room_food)

        other_room_food = food_in_room(121, TEST_DATABASE_FILENAME)
        self.assertCountEqual([other_food], other_room_food)
        self.assertNotEqual([food, other_food], other_room_food)

        connection.close()

    def test_getting_room_furniture(self):
        self.delete_furniture_table_rows()
        furniture = Furniture('sofa', 'excellent', 120)
        other_furniture = Furniture('chair', 'good', 121)
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Furniture(furniture) values (?)",
                       (furniture, ))
        cursor.execute("INSERT INTO Furniture(furniture) values (?)",
                       (other_furniture, ))
        connection.commit()

        room_furniture = furnitures_in_room(120, TEST_DATABASE_FILENAME)
        self.assertCountEqual([furniture], room_furniture)
        self.assertNotEqual([furniture, other_furniture], room_furniture)

        other_room_furniture = furnitures_in_room(121, TEST_DATABASE_FILENAME)
        self.assertCountEqual([other_furniture], other_room_furniture)
        self.assertNotEqual([furniture, other_furniture], other_room_furniture)

        connection.close()

    def test_getting_room_sleeping_furnitures(self):
        self.delete_sleeping_furniture_table_rows()
        furniture = SleepingFurniture('sofa', 'excellent', 5, 120)
        other_furniture = SleepingFurniture('bed', 'good', 6, 121)
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO SleepingFurniture(sf) values (?)",
                       (furniture, ))
        cursor.execute("INSERT INTO SleepingFurniture(sf) values (?)",
                       (other_furniture, ))
        connection.commit()

        room_furniture = sleeping_furnitures_in_room(120,
                                                     TEST_DATABASE_FILENAME)
        self.assertCountEqual([furniture], room_furniture)
        self.assertNotEqual([furniture, other_furniture], room_furniture)

        other_room_furniture = sleeping_furnitures_in_room(121,
                                                           TEST_DATABASE_FILENAME)
        self.assertCountEqual([other_furniture], other_room_furniture)
        self.assertNotEqual([furniture, other_furniture], other_room_furniture)

        connection.close()

    def test_change_food(self):
        self.delete_food_table_rows()

        maunfacture_date = date_to_string(date.today() - timedelta(days=20))
        first_expire_date = date_to_string(date.today() - timedelta(days=5))
        second_expire_date = date_to_string(date.today() + timedelta(days=10))

        food = Food('eggs', 5, maunfacture_date, first_expire_date, 120)
        other_food = Food('meat', 2, maunfacture_date, second_expire_date, 121)

        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Food(food) values (?)", (food, ))
        cursor.execute("INSERT INTO Food(food) values (?)", (other_food, ))
        connection.commit()

        cursor.execute('''Select * from Food''')
        foods = [convert_to_food(food[0]) for food in cursor.fetchall()]
        self.assertFalse(all(food.is_expire() is False for food in foods))
        self.assertTrue(any(food.is_expire() is True for food in foods))

        change_food(TEST_DATABASE_FILENAME)
        cursor.execute('''Select * from Food''')
        foods = [convert_to_food(food[0]) for food in cursor.fetchall()]
        self.assertTrue(all(food.is_expire() is False for food in foods))
        self.assertFalse(any(food.is_expire() is True for food in foods))
        connection.close()

    def test_change_bath_item(self):
        self.delete_bath_items_table_rows()

        last_replace_date = date_to_string(date.today() - timedelta(days=21))
        bath_item = BathItems('tooth brush', last_replace_date, 20, 120)
        other_bath_item = BathItems('shampoo', last_replace_date, 30, 121)

        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO BathItems(bath_items) values (?)",
                       (bath_item, ))
        cursor.execute("INSERT INTO BathItems(bath_items) values (?)",
                       (other_bath_item, ))
        connection.commit()

        cursor.execute('''Select * from BathItems''')
        bath_items = [convert_bath_item(bath_item[0])
                      for bath_item in cursor.fetchall()]
        self.assertFalse(all(bath_item.has_to_replace() is False
                         for bath_item in bath_items))
        self.assertTrue(any(bath_item.has_to_replace() is True
                        for bath_item in bath_items))

        change_bath_item(TEST_DATABASE_FILENAME)
        cursor.execute('''Select * from BathItems''')
        bath_items = [convert_bath_item(bath_item[0])
                      for bath_item in cursor.fetchall()]
        self.assertTrue(all(bath_item.has_to_replace() is False
                        for bath_item in bath_items))
        self.assertFalse(any(bath_item.has_to_replace() is True
                         for bath_item in bath_items))
        connection.close()

    def test_add_bath_item(self):
        self.delete_bath_items_table_rows()
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from BathItems''')

        self.assertCountEqual([], cursor.fetchall())
        bath_item = BathItems('tooth brush', "2014-7-10", 20, 120)
        other_bath_item = BathItems('shampoo', "2014-9-10", 20, 121)

        add_bath_item(bath_item, TEST_DATABASE_FILENAME)
        add_bath_item(other_bath_item, TEST_DATABASE_FILENAME)
        cursor.execute('''Select * from BathItems''')
        self.assertCountEqual([other_bath_item, bath_item],
                              [convert_bath_item(item[0])
                               for item in cursor.fetchall()])

    def test_add_food(self):
        self.delete_food_table_rows()
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from Food''')

        self.assertCountEqual([], cursor.fetchall())
        food = Food('eggs', 5, '2014-8-10', '2014-9-10', 120)
        other_food = Food('meat', 2, '2014-8-20', '2014-8-27', 121)

        add_food(food, TEST_DATABASE_FILENAME)
        add_food(other_food, TEST_DATABASE_FILENAME)
        cursor.execute('''Select * from Food''')
        self.assertCountEqual([other_food, food],
                              [convert_to_food(item[0])
                               for item in cursor.fetchall()])

    def test_add_furniture(self):
        self.delete_furniture_table_rows()
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from Furniture''')

        self.assertCountEqual([], cursor.fetchall())
        furniture = Furniture('sofa', 'excellent', 120)
        other_furniture = Furniture('chair', 'good', 121)

        add_furniture(furniture, TEST_DATABASE_FILENAME)
        add_furniture(other_furniture, TEST_DATABASE_FILENAME)
        cursor.execute('''Select * from Furniture''')
        self.assertCountEqual([other_furniture, furniture],
                              [convert_to_furniture(item[0])
                               for item in cursor.fetchall()])

    def test_add_sleeping_furniture(self):
        self.delete_sleeping_furniture_table_rows()
        connection = sqlite3.connect(TEST_DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute('''Select * from SleepingFurniture''')

        self.assertCountEqual([], cursor.fetchall())
        furniture = SleepingFurniture('sofa', 'excellent', 5, 120)
        other_furniture = SleepingFurniture('bed', 'good', 6, 121)

        add_sleeping_furniture(furniture, TEST_DATABASE_FILENAME)
        add_sleeping_furniture(other_furniture, TEST_DATABASE_FILENAME)
        cursor.execute('''Select * from SleepingFurniture''')
        self.assertCountEqual([other_furniture, furniture],
                              [convert_to_sleeping_furniture(item[0])
                               for item in cursor.fetchall()])

    def test_get_all_free_rooms_number(self):
        self.delete_room_table_rows()
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'True')
        third_room = Room(102, 40, 10, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)
        add_new_room(third_room, TEST_DATABASE_FILENAME)

        free_rooms = get_all_free_rooms_number(TEST_DATABASE_FILENAME)
        self.assertCountEqual([third_room.get_number, first_room.get_number],
                              free_rooms)
        self.assertNotEqual([third_room.get_number], free_rooms)
        self.assertNotEqual([third_room.get_number,
                             first_room.get_number,
                             second_room.get_number],
                            free_rooms)

    def test_get_all_rooms_number(self):
        self.delete_room_table_rows()
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'True')
        third_room = Room(102, 40, 10, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)
        add_new_room(third_room, TEST_DATABASE_FILENAME)

        rooms = get_all_rooms_number(TEST_DATABASE_FILENAME)
        self.assertNotEqual([third_room.get_number, first_room.get_number],
                            rooms)
        self.assertNotEqual([third_room.get_number], rooms)
        self.assertCountEqual([third_room.get_number,
                               first_room.get_number,
                               second_room.get_number], rooms)

    def test_get_room(self):
        self.delete_room_table_rows()
        first_room = Room(100, 20, 5, 'False')
        second_room = Room(101, 30, 6, 'True')
        third_room = Room(102, 40, 10, 'False')
        add_new_room(first_room, TEST_DATABASE_FILENAME)
        add_new_room(second_room, TEST_DATABASE_FILENAME)
        add_new_room(third_room, TEST_DATABASE_FILENAME)

        self.assertEqual(first_room, get_room(100, TEST_DATABASE_FILENAME))
        self.assertNotEqual(first_room, get_room(101, TEST_DATABASE_FILENAME))
        self.assertNotEqual(first_room, get_room(102, TEST_DATABASE_FILENAME))

        self.assertEqual(second_room, get_room(101, TEST_DATABASE_FILENAME))
        self.assertNotEqual(second_room, get_room(100, TEST_DATABASE_FILENAME))
        self.assertNotEqual(second_room, get_room(102, TEST_DATABASE_FILENAME))

        self.assertEqual(third_room, get_room(102, TEST_DATABASE_FILENAME))
        self.assertNotEqual(third_room, get_room(101, TEST_DATABASE_FILENAME))
        self.assertNotEqual(third_room, get_room(100, TEST_DATABASE_FILENAME))
