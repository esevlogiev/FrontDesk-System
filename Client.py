import time
from room import RoomNumber, Room


class Client:
	def __init__(self, first_name, last_name, phone_number, number_room, stay):
		self.date_registere = ""
		self.first_name = first_name
		self.last_name = last_name
		self.number_room = number_room
		self.time_stay = stay
		self.phone_number = phone_number

	def __str__(self):
		return self.first_name + ' ' + self.last_name + ' is registered on '\
		       + self.date_registere + ' in room ' + str(self.number_room)

	def get_first_name(self):
		return self.first_name

	def get_last_name(self):
		return self.last_name

	def get_phone_number(self):
		return self.phone_number

	def get_number_room(self):
		return number_room

	def set_number_room(self, number):
		self.number_room = number

	def get_time_stay(self, number):
		return self.time_stay

	def set_stay(self, days):
		self.time_stay = days

	def set_date_registere(self, date):
		self.date_registere = date

	def try_rent_room(self, room):
		if room.is_rent:
			return False
		room.is_rent = True
		self.date_registere = time.strftime("%d/%m/%Y")
		return True
