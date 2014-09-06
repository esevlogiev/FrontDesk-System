import sqlite3
import time

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classes.room import RoomNumber, Room


class Client:
    def __init__(self, first_name, last_name, phone_number, number_room, stay,
                 date_registere):
        self.date_registere = date_registere
        self.first_name = first_name
        self.last_name = last_name
        self.number_room = number_room
        self.time_stay = stay
        self.phone_number = phone_number

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%s;%i;%i;%s" % (self.first_name, self.last_name,
                                          self.phone_number, self.number_room,
                                          self.time_stay, self.date_registere)

    def __str__(self):
        return (self.first_name + ' ' + self.last_name + ' with phone ' +
                self.phone_number + ' is registered on ' +
                self.date_registere + ' in room ' + str(self.number_room))

    @property
    def get_first_name(self):
        return self.first_name

    @property
    def get_last_name(self):
        return self.last_name

    @property
    def get_phone_number(self):
        return self.phone_number

    @property
    def get_number_room(self):
        return self.number_room

    def set_number_room(self, number):
        self.number_room = number

    @property
    def get_time_stay(self):
        return self.time_stay

    def set_stay(self, days):
        self.time_stay = days

    def set_date_registere(self, date):
        self.date_registere = date

    @property
    def get_date_registere(self):
        return self.date_registere

    def try_rent_room(self, room):
        if room.is_rent:
            return False
        room.is_rent = True
        self.date_registere = time.strftime("%d/%m/%Y")
        return True

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
