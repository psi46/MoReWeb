
import os
import subprocess
import sys
sys.path.insert(1,"../")
from myutils import sClient,decode,printer,preexec
from shutil import copyfile
import time
import el_agente


class watchDog_agente(el_agente.el_agente):
    def __init__(self,timestamp,log,sclient):
        el_agente.el_agente.__init__(self, timestamp, log, sclient) 
        self.agente_name = "watchDogAgente"
        self.client_name = "watchDog"
        self.log = printer()
        self.sclient = sclient
        self.active = True
        self.pending = False
        self.currentTestTempLogger = None
        
    def setup_configuration(self, conf):
        #self.port = conf.get("jumoClient","port")
        self.logDir = conf.Directories['logDir']
        self.configFile = conf.Directories['configDir']+'/elComandante.conf'
        self.initFile = conf.Directories['configDir']+'/elComandante.ini'
#                                       get("Directories","dataDir")+"logfiles"
        self.logFileName = "temperature.log"
        self.subscription = "/temperature/jumo"
        self.tempLog = printer()
        self.tempLog.set_name('Temperature')
        self.tempLog.set_logfile('%s/%s'%(self.logDir,self.logFileName))
        self.tempLog.disable_print()
        return True
    
    def setup_initialization(self, init):
        return True;
    def check_logfiles_presence(self):
        return []
    def check_subscription(self):
        return True

    def check_client_running(self):
        return False

    def start_client(self, timestamp):
        try:
            self.sclient.subscribe(self.subscription)
            return True
        except:
            return False

    
    def subscribe(self):
        if(self.active):
            self.sclient.subscribe(self.subscription)

    def request_client_exit(self):
        # Request the client to exit with a command
        # through subsystem
        if not self.active:
            return True
        self.sclient.unsubscribe(self.subscription)
        return True
    def kill_client(self):
    # Kill a client with a SIGTERM signal
        if not self.active:
            return True
        return True


    def prepare_test(self, test, environment):
        # Run before a test is executed
        if not self.active:
            return True
        #self.log << "%s: Preparing %s @ %s..." % (self.agente_name, test,environment.name)
        self.currentTest = test
        self.readTemperatures()
        return True

    def execute_test(self):
        # Initiate a test
        #self.log << "%s: execute Test \'%s\'" % (self.agente_name, self.currentTest)
        self.readTemperatures()
#        self.currentTestTempLogger = logging.getLogger('%sTemplog'%self.currentTest)
#        self.currentTestTempLogger.handler = logging.FileHandler('%s/temperature.log')
        return True


    def cleanup_test(self):
        self.currentTest = "none"
        # Run after a test has executed
        self.readTemperatures()
        if not self.active:
            return True
        #if 'waiting' not in self.status()
        #    self.log << "%s: Cleaning up %s ..."%(self.agente_name,test)
        return False

    
    def final_test_cleanup(self):
        # Cleanup after all tests have finished to return
        # everything to the state before the test

        # create Config directory
        return False
    def check_finished(self):
        # Check whether the client has finished its task
        # but also check for errors and raise an exception
        # if one occurs.
        self.readTemperatures()
        return True

    def readTemperatures(self):
        packet = self.sclient.getFirstPacket(self.subscription)
        if not packet.isEmpty() and not "pong" in packet.data.lower():
            data = packet.data
            Time,coms,typ,msg = decode(data)[:4]
            if len(msg)>=1:
                self.tempLog << "%s\t %s"%(Time,msg[0])
        return True


    def set_pending(self):
        #self.sclient.send(self.subscription,":FINISHED\n")
        self.pending = True
        

