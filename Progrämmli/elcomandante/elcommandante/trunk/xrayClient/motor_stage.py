class motor_stage():
	def __init__(self, dimensions):
		self.dimensions = dimensions
	def is_open(self):
		return False
	def test_communication(self):
		return False
	def move_absolute(self, coordinates):
		return None
	def move_relative(self, coordinates):
		return None
	def set_acceleration(self, acceleration):
		return None
	def home(self):
		return None
	def reset(self):
		return None
