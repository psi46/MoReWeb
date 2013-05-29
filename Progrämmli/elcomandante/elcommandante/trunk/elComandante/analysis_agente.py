import os
import time
import subprocess

from myutils import process

import el_agente

def preexec():
    os.setpgrp()

class analysis_agente(el_agente.el_agente):
    def __init__(self, timestamp, log, sclient):
        el_agente.el_agente.__init__(self, timestamp, log, sclient)
        self.active = 1
        self.pending = False
        self.agente_name = "analysisAgente"
        self.client_name = "analysisClient"
        self.currentTest = 'none'
    def setup_configuration(self, conf):
        self.subscription = conf.get("subsystem", "analysisSubscription")
        self.log_dir = conf.get("Directories", "dataDir") + "/logfiles/"
        # FIXME: this is not correct
        self.exec_dir = conf.get("Directories", "dataDir")
        self.data_dir = conf.get("Directories", "dataDir")
        self.script_dir = conf.get("Directories", "scriptDir")
        self.conf = conf
        return True
    def setup_initialization(self, init):
        self.init = init
        self.directories = []
        tb = -1
        while True:
            tb += 1
            try:
                name = init.get("Modules", "TB%i" % tb)
                use = init.getboolean("TestboardUse", "TB%i" % tb)
                if not use:
                    continue
                date = time.strftime("%Y-%m-%d_%Hh%Mm", time.gmtime(self.timestamp))
                self.directories.append(self.data_dir + ("/%s_%s_%s/" % (name, date, self.timestamp)))
            except:
                break
        return True
    def check_logfiles_presence(self):
        # Returns a list of logfiles present in the filesystem
        return []
    def check_client_running(self):
        # Check whether a client process is running
        if not self.active:
            return False
        if process.check_process_running(self.client_name + ".py"):
            raise Exception("Another %s is already running. Please close this client first." % self.client_name)
            return True
        return False
    def start_client(self, timestamp):
        if not self.active:
            return True
        command = "xterm +sb -geometry 120x20+0+200 -fs 10 -fa 'Mono' -e "
        command += "python ../analysisClient/analysisClient.py "
        command += "--timestamp {0:d} ".format(timestamp)
        command += "--exec-dir {0:s} ".format(self.exec_dir)
        command += "--script-dir {0:s} ".format(self.script_dir)
        command += "--log-dir {0:s} ".format(self.log_dir)
        self.log << "Starting " + self.client_name + " ..."
        self.child = subprocess.Popen(command, shell = True, preexec_fn = preexec)
        return True
    def subscribe(self):
        self.sclient.subscribe(self.subscription)
    def check_subscription(self):
        # Verify the subsystem connection
        return self.sclient.checkSubscription(self.subscription)
    def request_client_exit(self):
        # Request the client to exit with a command
        # through subsystem
        self.sclient.send(self.subscription, ":EXIT\n")
        return True
    def kill_client(self):
        # Kill a client with a SIGTERM signal
        try:
            self.child.kill()
        except:
            pass
        return True
    def prepare_test(self, test, environment):
        # Run before a test is executed
        self.currentTest = test
        return True
    def execute_test(self):
        # Initiate a test
        # Get the command line and replace the spaces with commas
        # to send it through the subsystem
        try:
            command = self.init.get("Analysis " + self.currentTest, "command").split()
        except:
            # This is not an analysis
            return True
        self.log << "%s: Executing %s" % (self.client_name, " ".join(command))
        command = ",".join(command)
        for dir in self.directories:
            self.sclient.send(self.subscription, ":ANALYZE:EXECDIR " + dir + "\n")
            self.sclient.send(self.subscription, ":ANALYZE:EXECUTE " + command + "\n")
        self.set_pending()
        return True
    def cleanup_test(self):
        self.currentTest = 'none'
        # Run after a test has executed
        return True
    def final_test_cleanup(self):
        # Cleanup after all tests have finished to return
        # everything to the state before the test
        return True
    def check_finished(self):
        if not self.active or not self.pending:
            return True

        packet = self.sclient.getFirstPacket(self.subscription)
        if not packet.isEmpty():
            if "FINISHED" in packet.data.upper():
                    self.pending = False
            elif "ERROR" in packet.data.upper():
                self.pending = False
                self.log.warning("Error from %s" % self.client_name)
                #raise Exception("Error from %s" % self.client_name)

        return not self.pending
    def set_pending(self):
        self.sclient.send(self.subscription, ":FINISHED\n")
        self.pending = True
