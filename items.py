class Item:
	def __init__(self, name, _type):
		self.name = name
		self._type = _type

	def get_type(self):
		return self._type

	def get_name(self):
		return self.name

	def set_name(self, value):
		if value == "":
			print("Invalid null or empty value")
		else:
			self.name = name

	def __str__(self):
		return self.name + ' from type ' + self._type
