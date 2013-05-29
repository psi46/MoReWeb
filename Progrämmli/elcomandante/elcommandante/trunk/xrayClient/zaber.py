import struct
import serial

from motor_stage import motor_stage

class zaber_motor_stage(motor_stage):
	def __init__(self, device):
		motor_stage.__init__(self, 1)
		self.serialdevice = device
		self.serial = serial.Serial(device)
	def __del__(self):
		self.serial.close()
	def is_open(self):
		return self.serial.isOpen()
	def test_communication(self):
		answer = self.serial_command_with_response(55, 12345)
		return answer == self.make_packet(55, 12345)
	def move_absolute(self, coordinates):
		if type(coordinates) != list or len(coordinates) != self.dimensions:
			return 0
		answer = self.serial_command_with_response(20, coordinates[0])
		return answer != ""
	def move_relative(self, coordinates):
		if type(coordinates) != tuple or len(coordinates) != self.dimension:
			return 0
		answer = self.serial_command_with_response(21, coordinates[0])
		return answer != ""
	def set_acceleration(self, acceleration):
		answer = self.serial_command_with_response(43, acceleration)
		return answer != ""
	def home(self):
		answer = self.serial_command_with_response(21, 0)
		if answer == "":
			return 0
		answer = self.serial_command_with_response(1, 0)
		return answer != ""
	def reset(self):
		self.serial_command_no_response(0, 0)
		return True

	def make_packet(self, command, data):
		return struct.pack("<b", 1) + struct.pack("<b", command) + struct.pack("<i", data)
	def serial_command_no_response(self, command, data):
		packet = self.make_packet(command, data)
		self.serial.write(packet)
	def serial_command_with_response(self, command, data):
		packet = self.make_packet(command, data)
		self.serial.write(packet)
		answer = self.serial.read(6)
		return answer
