from Items import Item
import sqlite3


#to be a structure
class FurnitureQuality:
    def __init__(self, quality):
        self.quality = quality

    def __str__(self):
        return self.quality + " quality"


class Furniture(Item):
    def __init__(self, name, quality):
        Item.__init__(self, name, "furniture")
        FurnitureQuality.__init__(self, quality)

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s" % (self.name, self.quality)

    def get__quality(self):
        return self.quality

    def set_quality(self, value):
        self.quality = value

    def __str__(self):
        return Item.__str__(self) + " with " + FurnitureQuality.__str__(self)


class SleepingFurniture(Furniture):
    def __init__(self,name, quality, sleeping_seats):
        Furniture.__init__(self, quality, name)
        self.sleeping_seats = sleeping_seats

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%i" % (self.name,self.quality, self.sleeping_seats)
                                    

    def get_sleeping_seats(self):
        return self.sleeping_seats

    def set_sleeping_seats(self, value):
        if value > 0:
            self.sleeping_seats = value

    def __str__(self):
        return Furniture.__str__(self) + " and " + str(self.sleeping_seats) + " sleeping seats"
