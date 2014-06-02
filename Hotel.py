import room
import Client


class Hotel:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.rooms = []
        self.clients = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_rooms(self):
        return self.rooms

    def set_rooms(self, rooms):
        self.rooms = rooms

    def get_clients(self):
        return self.clients

    def set_clients(self, clients):
        self.clients = clients

    def get_available_rooms(self):
        result = []
        for room in self.rooms:
            if not room.is_rent:
                result.append(room)
        return result