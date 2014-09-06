import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest

from classes.bath_items import BathItems
from classes.client import Client
from classes.food import Food
from classes.room import Room
from classes.sleeping_furniture import Furniture, SleepingFurniture
from datetime import date, timedelta
from management.client_management import date_to_string


class BathItemsTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_with_wrong_arguemnts(self):
        self.assertRaises(TypeError, BathItems, 'missing 4 required positional\
                                                 arguments')

    def test_property_decorator(self):
        bath_item = BathItems('tooth brush', "2014-10-10", 20, 120)
        self.assertRaises(AttributeError, get_room_number=121)
        self.assertRaises(AttributeError, get_name="mirror")
        self.assertRaises(AttributeError, get_replace_period=10)
        self.assertRaises(AttributeError, get_last_replace_date="2014-10-11")

    def test_initialization(self):
        bath_item = BathItems('tooth brush', "2014-10-10", 20, 120)
        self.assertEqual(bath_item.get_name, 'tooth brush')
        self.assertNotEqual(bath_item.get_name, 'teeth brush')
        self.assertEqual(bath_item.get_room_number, 120)
        self.assertNotEqual(bath_item.get_room_number, 121)
        self.assertEqual(bath_item.get_replace_period, 20)
        self.assertNotEqual(bath_item.get_replace_period, 10)
        self.assertEqual(bath_item.get_last_replace_date, '2014-10-10')
        self.assertNotEqual(bath_item.get_last_replace_date, '2014-10-11')

    def test_type_correctness(self):
        bath_item = BathItems('tooth brush', "2014-10-10", 20, 120)
        self.assertTrue(bath_item.get_name, str)
        self.assertTrue(bath_item.get_last_replace_date, str)
        self.assertTrue(bath_item.get_room_number, int)
        self.assertTrue(bath_item.get_replace_period, int)

    def test_has_to_replace(self):
        last_replace_date = date_to_string(date.today() - timedelta(days=21))
        bath_item = BathItems('tooth brush', last_replace_date, 30, 120)
        self.assertFalse(bath_item.has_to_replace())

        other_bath_item = BathItems('shampoo', last_replace_date, 20, 121)
        self.assertTrue(other_bath_item.has_to_replace())

    def test_is_instance(self):
        self.assertIsInstance(BathItems('tooth brush', "2014-10-10", 20, 120),
                              BathItems, 'this object is not' +
                                         'instance of this class')
        self.assertNotIsInstance(BathItems('tooth brush', "2014-10-10", 20,
                                           120), Client)


class ClientTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_with_wrong_arguemnts(self):
        self.assertRaises(TypeError, Client, 'missing 6 required positional\
                                              arguments')

    def test_property_decorator(self):
        client = Client('Roger', 'Federer', '0898671234', 120, 5, '2014-08-20')
        self.assertRaises(AttributeError, get_first_name='Rafael')
        self.assertRaises(AttributeError, get_last_name='Nadal')
        self.assertRaises(AttributeError, get_phone_number='0888888888')
        self.assertRaises(AttributeError, get_number_room=130)
        self.assertRaises(AttributeError, get_time_stay=10)
        self.assertRaises(AttributeError, get_date_registere="2014-10-11")

    def test_initialization(self):
        client = Client('Roger', 'Federer', '0898671234', 120, 5, '2014-08-20')
        self.assertEqual(client.get_first_name, 'Roger')
        self.assertNotEqual(client.get_last_name, 'Rafael')
        self.assertEqual(client.get_last_name, 'Federer')
        self.assertNotEqual(client.get_last_name, 'Nadal')
        self.assertEqual(client.get_phone_number, '0898671234')
        self.assertNotEqual(client.get_phone_number, '0888888888')
        self.assertEqual(client.get_number_room, 120)
        self.assertNotEqual(client.get_number_room, 130)
        self.assertEqual(client.get_time_stay, 5)
        self.assertNotEqual(client.get_time_stay, 20)
        self.assertEqual(client.get_date_registere, '2014-08-20')
        self.assertNotEqual(client.get_date_registere, '2014-10-20')

    def test_type_correctness(self):
        client = Client('Roger', 'Federeer', '0898671234', 120, 5,
                        '2014-08-20')
        self.assertTrue(client.get_first_name, str)
        self.assertTrue(client.get_last_name, str)
        self.assertTrue(client.get_phone_number, str)
        self.assertTrue(client.get_number_room, int)
        self.assertTrue(client.get_time_stay, int)
        self.assertTrue(client.get_date_registere, str)

    def test_clients_equality(self):
        client = Client('Roger', 'Federer', '0898671234', 120, 5, '2014-08-20')
        other_client = Client('Rafael', 'Nadal', '0898671234', 120, 5,
                              '2014-08-20')
        self.assertEqual(client, Client('Roger', 'Federer', '0898671234',
                                        120, 5, '2014-08-20'))
        self.assertNotEqual(client, other_client)

    def test_is_instance(self):
        self.assertIsInstance(Client('Roger', 'Federer', '0898671234', 120, 5,
                                     '2014-08-20'), Client, 'this object is\
                                      not instance of this class')
        self.assertNotIsInstance(Client('Roger', 'Federer', '0898671234', 120,
                                        5, '2014-08-20'), BathItems)


class FoodTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_with_wrong_arguemnts(self):
        self.assertRaises(TypeError, Food, 'missing 5 required positional\
                                            arguments')

    def test_property_decorator(self):
        food = Food('Ice Cream', 3, '2014-8-10', '2014-9-10', 120)
        self.assertRaises(AttributeError, get_name='orange')
        self.assertRaises(AttributeError, get_quantity=5)
        self.assertRaises(AttributeError, get_manufacture_date='2014-10-10')
        self.assertRaises(AttributeError, get_expire_date='2014-11-11')
        self.assertRaises(AttributeError, get_room_number=130)

    def test_initialization(self):
        food = Food('Ice Cream', 3, '2014-8-10', '2014-9-10', 120)
        self.assertEqual(food.get_name, 'Ice Cream')
        self.assertNotEqual(food.get_name, 'Orange')
        self.assertEqual(food.get_quantity, 3)
        self.assertNotEqual(food.get_quantity, 5)
        self.assertEqual(food.get_manufacture_date, '2014-8-10')
        self.assertNotEqual(food.get_manufacture_date, '2014-9-10')
        self.assertEqual(food.get_expire_date, '2014-9-10')
        self.assertNotEqual(food.get_expire_date, '2014-10-10')
        self.assertEqual(food.get_room_number, 120)
        self.assertNotEqual(food.get_room_number, 130)

    def test_type_correctness(self):
        food = Food('Ice Cream', 3, '2014-8-10', '2014-9-10', 120)
        self.assertTrue(food.get_name, str)
        self.assertTrue(food.get_quantity, float)
        self.assertTrue(food.get_manufacture_date, str)
        self.assertTrue(food.get_expire_date, str)
        self.assertTrue(food.get_room_number, int)

    def test_food_equality(self):
        food = Food('Ice Cream', 3, '2014-8-10', '2014-9-10', 120)
        other_food = Food('Orange', 3, '2014-8-10', '2014-9-10', 120)
        self.assertEqual(food, Food('Ice Cream', 3, '2014-8-10', '2014-9-10',
                                    120))
        self.assertNotEqual(food, other_food)

    def test_is_food_expire(self):
        maunfacture_date = date_to_string(date.today() - timedelta(days=20))
        first_expire_date = date_to_string(date.today() - timedelta(days=5))
        second_expire_date = date_to_string(date.today() + timedelta(days=10))

        food = Food('eggs', 5, maunfacture_date, first_expire_date, 120)
        other_food = Food('meat', 2, maunfacture_date, second_expire_date, 121)
        self.assertTrue(food.is_expire())
        self.assertFalse(other_food.is_expire())

    def test_is_instance(self):
        food = Food('Ice Cream', 3, '2014-8-10', '2014-9-10', 120)
        self.assertIsInstance(food, Food,
                              'this object is not instance of this class')
        self.assertNotIsInstance(food, BathItems)


class RoomTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_with_wrong_arguemnts(self):
        self.assertRaises(TypeError, Room, 'missing 4 required positional\
                                            arguments')

    def test_property_decorator(self):
        room = Room(120, 20, 5, 'False')
        self.assertRaises(AttributeError, get_number=121)
        self.assertRaises(AttributeError, get_price_per_day=30.5)
        self.assertRaises(AttributeError, get_capacity=10)
        self.assertRaises(AttributeError, get_is_rent='True')

    def test_initialization(self):
        room = Room(120, 20, 5, 'False')
        self.assertEqual(room.get_number, 120)
        self.assertNotEqual(room.get_number, 121)
        self.assertEqual(room.get_price_per_day, 20)
        self.assertNotEqual(room.get_price_per_day, 30.5)
        self.assertEqual(room.get_capacity, 5)
        self.assertNotEqual(room.get_capacity, 10)
        self.assertEqual(room.get_is_rent, 'False')
        self.assertNotEqual(room.get_is_rent, 'True')

    def test_type_correctness(self):
        room = Room(120, 20, 5, 'False')
        self.assertTrue(room.get_number, int)
        self.assertTrue(room.get_price_per_day, float)
        self.assertTrue(room.get_capacity, int)
        self.assertTrue(room.get_is_rent, str)

    def test_food_equality(self):
        room = Room(120, 20, 5, 'False')
        other_room = Room(130, 25, 7, 'True')
        self.assertEqual(room, Room(120, 20, 5, 'False'))
        self.assertNotEqual(room, other_room)

    def test_is_instance(self):
        room = Room(120, 20, 5, 'False')
        self.assertIsInstance(room, Room,
                              'this object is not instance of this class')
        self.assertNotIsInstance(room, Food)


class FurnitureTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_with_wrong_arguemnts(self):
        self.assertRaises(TypeError, Furniture, 'missing 3 required positional\
                                            arguments')

    def test_property_decorator(self):
        furniture = Furniture('sofa', 'excellent', 120)
        self.assertRaises(AttributeError, get_name='bed')
        self.assertRaises(AttributeError, get_quality='good')
        self.assertRaises(AttributeError, get_room_number=130)

    def test_initialization(self):
        furniture = Furniture('sofa', 'excellent', 120)
        self.assertEqual(furniture.get_name, 'sofa')
        self.assertNotEqual(furniture.get_name, 'bed')
        self.assertEqual(furniture.get_quality, 'excellent')
        self.assertNotEqual(furniture.get_quality, 'bad')
        self.assertEqual(furniture.get_room_number, 120)
        self.assertNotEqual(furniture.get_room_number, 130)

    def test_type_correctness(self):
        furniture = Furniture('sofa', 'excellent', 120)
        self.assertTrue(furniture.get_name, str)
        self.assertTrue(furniture.get_quality, str)
        self.assertTrue(furniture.get_room_number, int)

    def test_food_equality(self):
        furniture = Furniture('sofa', 'excellent', 120)
        other_furniture = Furniture('bed', 'good', 130)
        self.assertEqual(furniture, Furniture('sofa', 'excellent', 120))
        self.assertNotEqual(furniture, other_furniture)

    def test_is_instance(self):
        furniture = Furniture('sofa', 'excellent', 120)
        self.assertIsInstance(furniture, Furniture,
                              'this object is not instance of this class')
        self.assertNotIsInstance(furniture, Food)


class SleepingFurnitueTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_with_wrong_arguemnts(self):
        self.assertRaises(TypeError, SleepingFurniture,
                          'missing 4 required positional arguments')

    def test_property_decorator(self):
        sleeping_furniture = SleepingFurniture('sofa', 'excellent', 2, 120)
        self.assertRaises(AttributeError, get_name='bed')
        self.assertRaises(AttributeError, get_quality='good')
        self.assertRaises(AttributeError, get_sleeping_seats=3)
        self.assertRaises(AttributeError, get_room_number=130)

    def test_initialization(self):
        sleeping_furniture = SleepingFurniture('sofa', 'excellent', 2, 120)
        self.assertEqual(sleeping_furniture.get_name, 'sofa')
        self.assertNotEqual(sleeping_furniture.get_name, 'bed')
        self.assertEqual(sleeping_furniture.get_quality, 'excellent')
        self.assertNotEqual(sleeping_furniture.get_quality, 'bad')
        self.assertEqual(sleeping_furniture.get_sleeping_seats, 2)
        self.assertNotEqual(sleeping_furniture.get_sleeping_seats, 3)
        self.assertEqual(sleeping_furniture.get_room_number, 120)
        self.assertNotEqual(sleeping_furniture.get_room_number, 130)

    def test_type_correctness(self):
        sleeping_furniture = SleepingFurniture('sofa', 'excellent', 2, 120)
        self.assertTrue(sleeping_furniture.get_name, str)
        self.assertTrue(sleeping_furniture.get_quality, str)
        self.assertTrue(sleeping_furniture.get_sleeping_seats, int)
        self.assertTrue(sleeping_furniture.get_room_number, int)

    def test_food_equality(self):
        sleeping_furniture = SleepingFurniture('sofa', 'excellent', 2, 120)
        other_sleeping_furniture = SleepingFurniture('bed', 'good', 3, 130)
        self.assertEqual(sleeping_furniture,
                         SleepingFurniture('sofa', 'excellent', 2, 120))
        self.assertNotEqual(sleeping_furniture, other_sleeping_furniture)

    def test_is_instance(self):
        sleeping_furniture = SleepingFurniture('sofa', 'excellent', 2, 120)
        self.assertIsInstance(sleeping_furniture, Furniture,
                              'this object is not instance of this class')
        self.assertIsInstance(sleeping_furniture, SleepingFurniture,
                              'this object is not instance of this class')
        self.assertNotIsInstance(sleeping_furniture, Food)
