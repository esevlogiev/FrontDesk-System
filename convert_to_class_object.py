import BathItems, Food, SleepingFurniture
from room import Room

def convert_room(room):
    l = room.split(";")
    return Room(l[0], l[1], l[2], l[3])

def convert_bath_item(bath_item):
    comp = bath_item.split(";")
    return BathItems(comp[0], comp[1], comp[2])

def convert_to_food(food):
    comp = food.split(";")
    return Food(comp[0], comp[1], comp[2])

def convert_to_furniture(furniture):
    comp = furniture.split(";")
    return Furniture(comp[0], comp[1])

def convert_to_sleeping_furniture(sleeping_furniture):
    comp = sleeping_furniture.split(";")
    return SleepingFurniture(comp[0], comp[1], comp[2])
