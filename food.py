import datetime
from Items import Item

class ExpirableItemBase:
    def __init__(self, manufacture_date, date_of_expire):
        self.manufacture_date = manufacture_date
        self.date_of_expire = date_of_expire

    #оправи да има водещи нули пред дните и месеците
    def is_expire(self):
        current_date = datetime.datetime.now()
        return current_date.isoformat()[:10] >= self.date_of_expire

    def __str__(self):
        return "made on " + self.manufacture_date + ", expired on "\
               + self.date_of_expire

class Food(ExpirableItemBase, Item):
    def __init__(self, name, quantity, manufacture_date, date_of_expire):
        ExpirableItemBase.__init__(self, manufacture_date, date_of_expire)
        Item.__init__(self, name, "Food")
        self.quantity = quantity

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%s;%s" % (self.name, self.quantity, self.manufacture_date,
                                    self.date_expire)

    def set_quantity(self, value):
        #направи да хвърля exception
        if value < 0:
            print("Error!!!")
        else:
            self.quantity = value

    def consume(self, some_food):
        if self.quantity - some_food > 0:
            self.quantity -= some_food
        else:
            self.quantity = 0
            #exception
            print("You can't eat more than there is!")

    def add_food(self, quantity):
        if quantity > 0:
            self.quantity += quantity

    def __str__(self):
        return self.name + " with quantity " + str(self.quantity) +\
               " " + ExpirableItemBase.__str__(self)
