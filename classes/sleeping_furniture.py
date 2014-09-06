import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.items import Item
import sqlite3


class FurnitureQuality:
    def __init__(self, quality):
        self.quality = quality

    def __str__(self):
        return self.quality + " quality"


class Furniture(Item):
    def __init__(self, name, quality, room_number):
        Item.__init__(self, name, "furniture")
        FurnitureQuality.__init__(self, quality)
        self.room_number = room_number

    def __str__(self):
        return Item.__str__(self) + " with " + FurnitureQuality.__str__(self)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%i" % (self.name, self.quality,
                                 self.room_number)

    @property
    def get_quality(self):
        return self.quality

    @property
    def set_quality(self, value):
        self.quality = value

    @property
    def get_room_number(self):
        return self.room_number


class SleepingFurniture(Furniture):
    def __init__(self, name, quality, sleeping_seats, room_number):
        Furniture.__init__(self, name, quality, room_number)
        self.sleeping_seats = sleeping_seats

    def __str__(self):
        return (Furniture.__str__(self) + " and " +
                str(self.sleeping_seats) + " sleeping seats")

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%i;%i" % (self.name, self.quality,
                                    self.sleeping_seats, self.room_number)

    @property
    def get_sleeping_seats(self):
        return self.sleeping_seats

    def set_sleeping_seats(self, value):
        if value > 0:
            self.sleeping_seats = value
