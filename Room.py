import SleepingFurniture
import sqlite3

class RoomNumber:
    def __init__(self, floor, number):
        self.floor = floor
        self.number = number

    def room_number(self):
        return self.number

    def room_floor(self):
        return self.floor

    def __str__(self):
        return str(self.number) + " room is on " + " floor " + str(self.floor)

class Room:
    def __init__(self, number, price_per_day, capacity, is_rent):
        self.number = number
        self.items = []
        self.price_per_day = price_per_day
        self.is_rent = is_rent
        self.capacity = capacity

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%i;%f;%i;%s" % (self.number, self.price_per_day,
                                    self.capacity, self.is_rent)

    def is_rent(self):
        return self.is_rent

    def set_is_rent(self, is_rent):
        self.is_rent = is_rent

    def get_number(self):
        return RoomNumber(self)

    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items

    def get_capacity(self):
        return self.capacity

    def get_price_per_day(self):
        return self.price_per_day

    def calculate_price(self, days):
        return self.price_per_day * days
