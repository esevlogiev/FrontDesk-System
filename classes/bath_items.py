import sqlite3
from datetime import date

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import classes.items

class BathItems:
    def __init__(self, name, last_replace_date, replace_period, room_number):
        self.last_replace_date = last_replace_date
        self.name = name
        self.type = "BathItem"
        self.replace_period = replace_period
        self.room_number = room_number

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%i;%i" % (self.name, self.last_replace_date,
                                    self.replace_period, self.room_number)
    @property
    def get_name(self):
        return self.name

    @property
    def get_last_replace_date(self):
        return self.last_replace_date

    @property
    def get_replace_period(self):
        return self.replace_period

    @property
    def get_room_number(self):
        return self.room_number

    def replace(self):
        today = date.today()
        self.last_replace_date = str(today.year) + '-' + str(today.month) +\
                                 '-' + str(today.day) 

    def has_to_replace(self):
        today = date.today()
        date_partition = self.last_replace_date.split('-')
        old_year, old_month, old_day = date_partition[0], date_partition[1],\
                                       date_partition[2]
        current_date = date(today.year, today.month, today.day)
        old_date = date(int(old_year), int(old_month),int(old_day))
        delta = current_date - old_date
        return delta.days > self.replace_period

    def __str__(self):
        return self.name + " from type " + self.type + " is last replace on "\
              + self.last_replace_date + " with replace period of " \
              + str(self.replace_period) + " days"

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False