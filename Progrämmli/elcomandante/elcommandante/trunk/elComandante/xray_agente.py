import os
import subprocess

from myutils import process
import el_agente

def preexec():
	os.setpgrp()

class xray_agente(el_agente.el_agente):
	def __init__(self, timestamp, log, sclient):
		el_agente.el_agente.__init__(self, timestamp, log, sclient)
		self.agente_name = "xrayAgente"
		self.client_name = "xrayClient"
		self.hvon = False
		self.beamon = False
		self.voltage = None
		self.current = None
		self.target = None
	def setup_configuration(self, conf):
		self.xray_type = conf.get("xrayClient", "xrayType")
		self.xray_device = conf.get("xrayClient", "xrayDevice")
		self.xrf_type = conf.get("xrayClient", "xrfType")
		self.xrf_device = conf.get("xrayClient", "xrfDevice")
		self.targets = conf.get("xrayClient", "xrfTargets")
		self.subscription = conf.get("subsystem", "xraySubscription")
		self.logdir = conf.get("Directories", "dataDir") + "/logfiles/"
		return True
	def setup_initialization(self, init):
		self.active = init.getboolean("Xray", "XrayUse")
		return True
	def check_client_running(self):
		if not self.active:
			return False
		if process.check_process_running(self.client_name + ".py"):
			raise Exception("Another %s is already running. Please close this client first." % self.client_name)
			return True
		return False
	def start_client(self, timestamp):
		if not self.active:
			return True
		command = "xterm +sb -geometry 120x20+0+300 -fs 10 -fa 'Mono' -e "
		command += "python ../xrayClient/xrayClient.py "
		command += "--timestamp {0:d} ".format(timestamp)
		command += "--directory {0:s} ".format(self.logdir)
		command += "--xray-device {0:s} ".format(self.xray_device)
		command += "--xray-type {0:s} ".format(self.xray_type)
		command += "--stage-device {0:s} ".format(self.xrf_device)
		command += "--stage-type {0:s} ".format(self.xrf_type)
		command += "--targets {0:s}".format(self.targets)
		self.log << "Starting " + self.client_name + " ..."
		self.child = subprocess.Popen(command, shell = True, preexec_fn = preexec)
		return True
	def subscribe(self):
		if (self.active):
			self.sclient.subscribe(self.subscription)
	def check_subscription(self):
		if (self.active):
			return self.sclient.checkSubscription(self.subscription)
		return True
	def request_client_exit(self):
		if not self.active:
			return True
		self.sclient.send(self.subscription, ":EXIT\n")
		return False
	def kill_client(self):
		if not self.active:
			return True
		try:
			self.child.kill()
		except:
			pass
		return True
	def prepare_test(self, test, environment):
		# Run before a test is executed
		if not self.active:
			return True
		if environment.xray:
			if environment.xray_voltage != self.voltage:
				self.sclient.send(self.subscription, ":SET:VOLTAGE %d\n" % environment.xray_voltage)
				self.voltage = environment.xray_voltage
			if environment.xray_current != self.current:
				self.sclient.send(self.subscription, ":SET:CURRENT %d\n" % environment.xray_current)
				self.current = environment.xray_current
			if environment.xray_target != self.target:
				self.sclient.send(self.subscription, ":SET:TARGET %s\n" % environment.xray_target)
				self.target = environment.xray_target
			if not self.hvon:
				self.sclient.send(self.subscription, ":SET:HV ON\n")
				self.hvon = True
			if not self.beamon:
				self.sclient.send(self.subscription, ":SET:BEAM ON\n")
				self.beamon = True
			self.set_pending()
		else:
			if self.beamon:
				self.sclient.send(self.subscription, ":SET:BEAM OFF\n")
				self.beamon = False
			if self.hvon:
				self.sclient.send(self.subscription, ":SET:HV OFF\n")
				self.hvon = False
			self.set_pending()
		return True
	def execute_test(self):
		# Runs a test
		if not self.active:
			return True
		return True
	def cleanup_test(self):
		# Run after a test has executed
		if not self.active:
			return True
		if self.beamon:
			self.sclient.send(self.subscription, ":SET:BEAM OFF\n")
			self.beamon = False
			self.set_pending()
		return True
	def final_test_cleanup(self):
		# Run after a test has executed
		if not self.active:
			return True
		self.sclient.send(self.subscription, ":SET:BEAM OFF\n")
		self.sclient.send(self.subscription, ":SET:HV OFF\n")
		self.set_pending()
		return True
	def check_finished(self):
		if not self.active:
			return True

		packet = self.sclient.getFirstPacket(self.subscription)
		if not packet.isEmpty():
			if self.pending and "FINISHED" in packet.data.upper():
				self.pending = False
			elif "ERROR" in packet.data.upper():
				self.pending = False
				raise Exception("Error from %s!" % self.client_name)

		return not self.pending
	def set_pending(self):
		self.sclient.send(self.subscription, ":FINISHED\n")
		self.pending = True
