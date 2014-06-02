import datetime
from Items import Item

class BathItems:
    def __init__(self,name, last_replace_date, replace_period):
        self.last_replace_date = last_replace_date
        self.name = name
        self.type = "BathItem"
        self.replace_period = replace_period

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%s" % (self.name, self.last_replace_date,
                                    self.replace_period)

    def replace(self, current_date):
        self.last_replace_date = current_date

    def has_to_replace(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        date_partition = self.last_replace_date.split()
        current_date = datetime.date(year, month, day)
        old_date = datetime.date(int(date_partition[0]), int(date_partition[1]),
                                 int(date_partition[2]))
        delta = current_date - old_date
        return delta.days > self.replace_period

    def __str__(self):
        return self.name + " from type " + self.type + " is last replace on "\
              + self.last_replace_date + " with replace period of " \
              + str(self.replace_period) + " days"
        
