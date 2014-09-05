import sqlite3



class RoomNumber:
    def __init__(self, floor, number):
        self.floor = floor
        self.number = number

    @property
    def room_number(self):
        return self.number

    @property
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
    @property
    def get_is_rent(self):
        return self.is_rent

    def set_is_rent(self, is_rent):
        self.is_rent = is_rent

    @property
    def get_number(self):
        return self.number

    @property
    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items

    @property
    def get_capacity(self):
        return self.capacity

    @property
    def get_price_per_day(self):
        return self.price_per_day

    def calculate_price(self, days):
        return self.price_per_day * days

    def __str__(self):
        return str(self.number) + ' ' + str(self.price_per_day) + ' '\
               + str(self.capacity) + ' ' + str(self.is_rent)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
        