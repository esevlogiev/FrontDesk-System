import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.room import Room
from classes.food import Food
from classes.client import Client
from classes.sleeping_furniture import SleepingFurniture, Furniture
from classes.bath_items import BathItems
from models.room_model import RoomModel, ROOM_CHARACTERISTICS
from models.client_model import ClientsModel, CLIENT_CHARACTERISTICS
from models.maid_model import MAID_CHARACTERISTICS, MaidModel
from models.sleeping_furniture_model import (SLEEPING_FURNITURE_CHARACTERISTICS,
                                             SleepingFurnituresModel)
from models.furniture_model import FURNITURE_CHARACTERISTICS, FurnituresModel
from models.bath_item_model import BathItemsModel, BATH_ITEM_CHARACTERISTICS
from models.food_model import FoodModel, FOOD_CHARACTERISTICS
from PyQt5.QtCore import Qt
import unittest


class ModelsTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_room_model(self):
        rooms = [Room(100, 20, 5, 'False'), Room(101, 30, 6, 'False'),
                 Room(102, 10, 7, 'True'), Room(103, 20, 10, 'True')]
        self.room_model = RoomModel()
        self.room_model.set_rooms(rooms)
        self.assertEqual(self.room_model.rowCount(), len(rooms))
        self.assertEqual(self.room_model.headerData(0, Qt.Horizontal,
                         Qt.DisplayRole), 'Room Number')
        self.assertEqual(self.room_model.headerData(1, Qt.Horizontal,
                         Qt.DisplayRole), 'Price Per Day')
        self.assertEqual(self.room_model.headerData(2, Qt.Horizontal,
                         Qt.DisplayRole), 'Capacity')
        self.assertEqual(self.room_model.headerData(3, Qt.Horizontal,
                         Qt.DisplayRole), 'Rent')
        getters = ('get_number', 'get_price_per_day', 'get_capacity',
                   'get_is_rent')
        for row in range(self.room_model.rowCount()):
            for column in range(ROOM_CHARACTERISTICS):
                self.assertEqual(getattr(rooms[row], getters[column]),
                                 self.room_model.data(self.room_model.index(
                                                      row, column),
                                                      Qt.DisplayRole))

    def test_client_model(self):
        clients = [Client('Roger', 'Federer', '0898671234', 100, 10,
                          '2014-10-10'),
                   Client('Rafael', 'Nadal', '0898671234', 101, 5,
                          '2014-9-15'),
                   Client('Novak', 'Djokovic', '0898645234', 102, 6,
                          '2014-12-15')]

        self.client_model = ClientsModel()
        self.client_model.set_clients(clients)
        self.assertEqual(self.client_model.rowCount(), len(clients))
        self.assertEqual(self.client_model.headerData(0, Qt.Horizontal,
                         Qt.DisplayRole), 'Room Number')
        self.assertEqual(self.client_model.headerData(1, Qt.Horizontal,
                         Qt.DisplayRole), 'First Name')
        self.assertEqual(self.client_model.headerData(2, Qt.Horizontal,
                         Qt.DisplayRole), 'Last Name')
        self.assertEqual(self.client_model.headerData(3, Qt.Horizontal,
                         Qt.DisplayRole), 'Phone Number')
        self.assertEqual(self.client_model.headerData(4, Qt.Horizontal,
                         Qt.DisplayRole), 'Stay')
        self.assertEqual(self.client_model.headerData(5, Qt.Horizontal,
                         Qt.DisplayRole), 'Date Registere')
        getters = ('get_number_room', 'get_first_name', 'get_last_name',
                   'get_phone_number', 'get_time_stay', 'get_date_registere')

        for row in range(self.client_model.rowCount()):
            for column in range(CLIENT_CHARACTERISTICS):
                self.assertEqual(getattr(clients[row], getters[column]),
                                 self.client_model.data(
                                 self.client_model.index(row, column),
                                 Qt.DisplayRole))

    def test_maid_model(self):
        maids = [('Georgi', 'Karapetrov'), ('Petyr', 'Todorov'),
                 ('Asen', 'Nikolov'), ('Kalin', 'Georgiev')]
        self.maid_model = MaidModel()
        self.maid_model.set_maids(maids)
        self.assertEqual(self.maid_model.rowCount(), len(maids))
        self.assertEqual(self.maid_model.headerData(0, Qt.Horizontal,
                         Qt.DisplayRole), 'First Name')
        self.assertEqual(self.maid_model.headerData(1, Qt.Horizontal,
                         Qt.DisplayRole), 'Last Name')
        for row in range(self.maid_model.rowCount()):
            for column in range(MAID_CHARACTERISTICS):
                self.assertEqual(maids[row][column],
                                 self.maid_model.data(self.maid_model.index(
                                                      row, column),
                                                      Qt.DisplayRole))

    def test_sleeping_furniture_model(self):
        sleeping_furnitures = [SleepingFurniture('sofa', 'excellent', 2, 120),
                               SleepingFurniture('bed', 'good', 1, 121),
                               SleepingFurniture('chair', 'bad', 4, 122)]
        self.sleeping_furnitures_model = SleepingFurnituresModel()
        self.sleeping_furnitures_model.set_sleeping_furnitures(
            sleeping_furnitures)
        self.assertEqual(self.sleeping_furnitures_model.rowCount(),
                         len(sleeping_furnitures))
        self.assertEqual(self.sleeping_furnitures_model.headerData(0,
                         Qt.Horizontal, Qt.DisplayRole), 'Room Number')
        self.assertEqual(self.sleeping_furnitures_model.headerData(1,
                         Qt.Horizontal, Qt.DisplayRole), 'Name')
        self.assertEqual(self.sleeping_furnitures_model.headerData(2,
                         Qt.Horizontal, Qt.DisplayRole), 'Quality')
        self.assertEqual(self.sleeping_furnitures_model.headerData(3,
                         Qt.Horizontal, Qt.DisplayRole), 'Sleeping Seats')

        getters = ('get_room_number', 'get_name', 'get_quality',
                   'get_sleeping_seats')
        for row in range(self.sleeping_furnitures_model.rowCount()):
            for column in range(SLEEPING_FURNITURE_CHARACTERISTICS):
                self.assertEqual(getattr(sleeping_furnitures[row],
                                         getters[column]),
                                 self.sleeping_furnitures_model.data(
                                 self.sleeping_furnitures_model.index(
                                 row, column), Qt.DisplayRole))

    def test_furniture_model(self):
        furnitures = [Furniture('sofa', 'excellent', 120),
                      Furniture('bed', 'good', 121),
                      Furniture('chair', 'bad', 122)]
        self.furnitures_model = FurnituresModel()
        self.furnitures_model.set_furnitures(furnitures)
        self.assertEqual(self.furnitures_model.rowCount(), len(furnitures))
        self.assertEqual(self.furnitures_model.headerData(0, Qt.Horizontal,
                         Qt.DisplayRole), 'Room Number')
        self.assertEqual(self.furnitures_model.headerData(1, Qt.Horizontal,
                         Qt.DisplayRole), 'Name')
        self.assertEqual(self.furnitures_model.headerData(2, Qt.Horizontal,
                         Qt.DisplayRole), 'Quality')

        getters = ('get_room_number', 'get_name', 'get_quality')
        for row in range(self.furnitures_model.rowCount()):
            for column in range(FURNITURE_CHARACTERISTICS):
                self.assertEqual(getattr(furnitures[row], getters[column]),
                                 self.furnitures_model.data(
                                 self.furnitures_model.index(row, column),
                                 Qt.DisplayRole))

    def test_bath_items_model(self):
        bath_items = [BathItems('tooth brush', "2014-10-10", 20, 120),
                      BathItems('soap', "2015-10-10", 30, 121),
                      BathItems('tooth paste', "2014-9-10", 40, 122)]
        self.bath_items_model = BathItemsModel()
        self.bath_items_model.set_bath_items(bath_items)
        self.assertEqual(self.bath_items_model.rowCount(), len(bath_items))
        self.assertEqual(self.bath_items_model.headerData(0, Qt.Horizontal,
                         Qt.DisplayRole), 'Room Number')
        self.assertEqual(self.bath_items_model.headerData(1, Qt.Horizontal,
                         Qt.DisplayRole), 'Name')
        self.assertEqual(self.bath_items_model.headerData(2, Qt.Horizontal,
                         Qt.DisplayRole), 'Last Replace Date')
        self.assertEqual(self.bath_items_model.headerData(3, Qt.Horizontal,
                         Qt.DisplayRole), 'Replace Period')

        getters = ('get_room_number', 'get_name', 'get_last_replace_date',
                   'get_replace_period')

        for row in range(self.bath_items_model.rowCount()):
            for column in range(BATH_ITEM_CHARACTERISTICS):
                self.assertEqual(getattr(bath_items[row], getters[column]),
                                 self.bath_items_model.data(
                                 self.bath_items_model.index(row, column),
                                 Qt.DisplayRole))

    def test_food_model(self):
        foods = [Food('Ice Cream', 3, '2014-8-10', '2014-9-10', 120),
                 Food('Chocolate', 2, '2014-9-10', '2014-10-10', 121),
                 Food('Tomato', 5, '2014-11-10', '2014-12-10', 122)]
        self.food_model = FoodModel()
        self.food_model.set_food(foods)
        self.assertEqual(self.food_model.rowCount(), len(foods))
        self.assertEqual(self.food_model.headerData(0, Qt.Horizontal,
                         Qt.DisplayRole), 'Room Number')
        self.assertEqual(self.food_model.headerData(1, Qt.Horizontal,
                         Qt.DisplayRole), 'Name')
        self.assertEqual(self.food_model.headerData(2, Qt.Horizontal,
                         Qt.DisplayRole), 'Quantity')
        self.assertEqual(self.food_model.headerData(3, Qt.Horizontal,
                         Qt.DisplayRole), 'Manufacture Date')
        self.assertEqual(self.food_model.headerData(4, Qt.Horizontal,
                         Qt.DisplayRole), 'Expire Date')

        getters = ('get_room_number', 'get_name', 'get_quantity',
                   'get_manufacture_date', 'get_expire_date')

        for row in range(self.food_model.rowCount()):
            for column in range(FOOD_CHARACTERISTICS):
                self.assertEqual(getattr(foods[row], getters[column]),
                                 self.food_model.data(self.food_model.index(
                                                      row, column),
                                                      Qt.DisplayRole))
