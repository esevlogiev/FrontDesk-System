import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.room import Room
from classes.food import Food
from classes.client import Client
from classes.bath_items import BathItems
from classes.sleeping_furniture import Furniture, SleepingFurniture


def convert_room(room):
    properties = room.split(";")
    return Room(int(properties[0]), float(properties[1]), int(properties[2]),
                properties[3])


def convert_bath_item(bath_item):
    properties = bath_item.split(";")
    return BathItems(properties[0], properties[1], int(properties[2]),
                     int(properties[3]))


def convert_to_food(food):
    properties = food.split(";")
    return Food(properties[0], float(properties[1]), properties[2],
                properties[3], int(properties[4]))


def convert_to_furniture(furniture):
    properties = furniture.split(";")
    return Furniture(properties[0], properties[1], int(properties[2]))


def convert_to_client(client):
    properties = client.split(";")
    return Client(properties[0], properties[1], properties[2],
                  int(properties[3]), int(properties[4]), properties[5])


def convert_to_sleeping_furniture(sleeping_furniture):
    properties = sleeping_furniture.split(";")
    return SleepingFurniture(properties[0], properties[1], int(properties[2]),
                             int(properties[3]))
