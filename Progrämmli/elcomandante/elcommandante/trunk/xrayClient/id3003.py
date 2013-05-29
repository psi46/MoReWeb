import struct
import serial
import time

from xray_generator import xray_generator

class id3003_xray_generator(xray_generator):
	def __init__(self, device):
		xray_generator.__init__(self, 4)
		self.serialdevice = device
		self.serial = serial.Serial(device)
	def __del__(self):
		self.serial.close()
	def is_open(self):
		return self.serial.isOpen()
	def test_communication(self):
		answer = self.serial_command_with_response("ID\n")
		return answer[:23] == "*- ISO-DEBYEFLEX 3003 -"

	def set_voltage(self, kV):
		if type(kV) != int or kV < 2 or kV > 60:
			return False
		command = "SV:{0:02d}\n".format(int(kV))
		self.serial_command_no_response(command)
		return self.get_voltage() == kV
	def get_voltage(self):
		answer = self.serial_command_with_response("VN\n")
		return int(answer[6:8])
	def set_current(self, mA):
		if type(mA) != int or mA < 2 or mA > 80:
			return False
		command = "SC:{0:02d}\n".format(int(mA))
		self.serial_command_no_response(command)
		return self.get_current() == mA
	def get_current(self):
		answer = self.serial_command_with_response("CN\n")
		return int(answer[6:8])
	def set_hv(self, on):
		if on:
			self.serial_command_no_response("HV:1\n")
		else:
			self.serial_command_no_response("HV:0\n")

		if self.get_hv() != on:
			return False

		if not on:
			return True

		# When turning on wait for voltage and current to settle
		answer = self.serial_command_with_response("VN\n")
		nominal_voltage = int(answer[1:-1])
		answer = self.serial_command_with_response("CN\n")
		nominal_current = int(answer[1:-1])
		actual_voltage = 0
		actual_current = 0
		trials = 0
		while actual_voltage != nominal_voltage or actual_current != nominal_current:
			if trials > 100:
				self.set_hv(0)
				return False
			answer = self.serial_command_with_response("VA\n")
			actual_voltage = int(answer[1:-1])
			answer = self.serial_command_with_response("CA\n")
			actual_current = int(answer[1:-1])
			trials += 1
			time.sleep(0.2)

		return True
	def get_hv(self):
		answer = self.serial_command_with_response("SR:01\n")
		return bool(int(answer[1:-1]) & (1 << 6))
	def set_beam_shutter(self, beamno, on):
		if beamno < 1 or beamno > 4:
			return False
		if on:
			command = "OS:{0:d}\n".format(beamno)
		else:
			command = "CS:{0:d}\n".format(beamno)
		self.serial_command_no_response(command)
		time.sleep(2)
		answer = ""
		if beamno == 1 or beamno == 2:
			answer = self.serial_command_with_response("SR:03\n")
		elif beamno == 3 or beamno == 4:
			answer = self.serial_command_with_response("SR:04\n")
		bit = 0
		if beamno == 1 or beamno == 3:
			bit = 6
		elif beamno == 2 or beamno == 4:
			bit = 2
		return bool(int(answer[1:-1]) & (1 << bit)) == bool(on)

	def serial_command_no_response(self, command):
		self.serial.write(unicode(command))
	def serial_command_with_response(self, command):
		self.serial.write(command)
		self.serial.flush()
		answer = ""
		while len(answer) == 0 or answer[-1] != '\r':
			answer += self.serial.read(1)
		return answer
