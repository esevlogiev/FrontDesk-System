import sqlite3
import datetime

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.items import Item


class ExpirableItemBase:
    def __init__(self, manufacture_date, date_of_expire):
        self.manufacture_date = manufacture_date
        self.date_of_expire = date_of_expire

    def is_expire(self):
        year, month, day = self.date_of_expire.split("-")
        return (datetime.date(int(year), int(month), int(day)) <
                datetime.date.today())

    def replace(self, new_manufacture_date, new_date_of_expire):
        self.manufacture_date = new_manufacture_date
        self.date_of_expire = new_date_of_expire

    def __str__(self):
        return "made on " + self.manufacture_date + ", expired on "\
               + self.date_of_expire


class Food(ExpirableItemBase, Item):
    def __init__(self, name, quantity, manufacture_date, date_of_expire,
                 room_number):
        ExpirableItemBase.__init__(self, manufacture_date, date_of_expire)
        Item.__init__(self, name, "Food")
        self.quantity = quantity
        self.room_number = room_number

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%f;%s;%s;%i" % (self.name, self.quantity,
                                       self.manufacture_date,
                                       self.date_of_expire,
                                       self.room_number)

    def set_quantity(self, value):
        if value < 0:
            print("Error!!!")
        else:
            self.quantity = value

    def consume(self, some_food):
        if self.quantity - some_food > 0:
            self.quantity -= some_food
        else:
            self.quantity = 0
            print("You can't eat more than there is!")

    def add_food(self, quantity):
        if quantity > 0:
            self.quantity += quantity

    @property
    def get_manufacture_date(self):
        return self.manufacture_date

    @property
    def get_expire_date(self):
        return self.date_of_expire

    @property
    def get_quantity(self):
        return self.quantity

    @property
    def get_room_number(self):
        return self.room_number

    def __str__(self):
        return (self.name + " with quantity " + str(self.quantity) +
                " " + ExpirableItemBase.__str__(self))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
