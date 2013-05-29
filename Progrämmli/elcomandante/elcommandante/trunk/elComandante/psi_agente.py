import os
import sys
sys.path.insert(1, "../")
from myutils import BetterConfigParser, sClient, decode, printer, preexec
from myutils import Testboard as Testboarddefinition
from time import strftime, gmtime, sleep
import time
from shutil import copytree,rmtree
import argparse
import environment
import signal
import el_agente
import subprocess


class psi_agente(el_agente.el_agente):
    def __init__(self, timestamp,log, sclient):
        el_agente.el_agente.__init__(self,timestamp, log, sclient)
        self.agente_name = "psiAgente"
        self.client_name = "psiClient"
        self.currenttest=None
        self.init = None
    def setup_configuration(self, conf):
        self.conf = conf
        self.subscription = conf.get("subsystem", "psiSubscription")
        self.highVoltageSubscription = conf.get("subsystem","keithleySubscription");
        #self.logdir = conf.get("Directories", "dataDir") + "/logfiles/"
        self.active = True
    def setup_initialization(self, init):
        self.init = init
        self.Testboards=[]
        for tb, module in init.items('Modules'):
            if init.getboolean('TestboardUse',tb):
                self.Testboards.append(Testboarddefinition(int(tb[2]),module,self.conf.get('TestboardAddress',tb),init.get('ModuleType',tb)))
                #Testboards[-1].tests=testlist
                self.Testboards[-1].defparamdir=self.Directories['defaultParameters']+'/'+self.conf.get('defaultParameters',self.Testboards[-1].type)
                self.log << '\t- Testboard %s at address %s with Module %s'%(self.Testboards[-1].slot,self.Testboards[-1].address,self.Testboards[-1].module)
        self.numTestboards = len(init.items('Modules'))
    def check_client_running(self):
        if not self.active:
            return False
        process = os.system("ps aux | grep -v grep | grep -v vim | grep -v emacs | grep %s" % self.client_name)
        if type(process) == str and process != "":
            raise Exception("Another %s self.sclient is already running. Please close this self.sclient first." % self.sclient.name)
            return True
        return False
    def subscribe(self):
        if (self.active):
            self.sclient.subscribe(self.subscription)

    def start_client(self, timestamp):
        self.timestamp = timestamp
        if not self.active:
            return True
        command = "xterm +sb -geometry 120x20+0+300 -fs 10 -fa 'Mono' -e "
        command += "python ../psiClient/psi46master.py "
        command += "-dir %s "%(self.Directories['logDir'])
        command += "-num %s"%self.numTestboards
        self.log << "Starting " + self.client_name + " ..."
        self.child = subprocess.Popen(command, shell = True, preexec_fn = preexec)
        return True

    def request_client_exit(self):
        if not self.active:
            return True
        self.sclient.send(self.subscription, ":EXIT\n")
        return False

    def kill_client(self):
        if not self.active:
            return True
        self.child.kill()
        return True
    def set_test(self, test):
        el_agente.el_agente.set_test(self, test)
        self.test.parameter_dir = list(test.parent.parameter_dir)

    def prepare_test(self, whichtest, env):
        if not self.active:
            return False
        # Run before a test is executed
        self.activeTestboard = -1
        self.powercycle()
        self.currenttest = whichtest.split('@')[0]
        if 'IV' in self.currenttest:
            activeTestboard = self.currenttest.split('_')
            if len(activeTestboard) == 2:
                self.currenttest = 'IV'
                self.activeTestboard = int(activeTestboard[1].strip('TB'))
                #print 'active testboard for IV is: %s'%self.activeTestboard
        for Testboard in self.Testboards:
            self._prepare_testboard(Testboard)
        self.pending = False
        return True

    def _prepare_testboard(self,Testboard):
        if 'IV' in self.currenttest:
            if Testboard.slot != self.activeTestboard:
                return
        if self.test.environment.temperature >=0:
            tempString = "p%s"%int(self.test.environment.temperature)
        else:
            tempString = "m%s"%(-1*int(self.test.environment.temperature))
             
        Testboard.testdir = Testboard.parentDir + '/%s_%s_%s/' % (str(Testboard.numerator).zfill(3), self.currenttest, tempString)
        self.log <<"%s: set testdir '%s'"%(self.agente_name,Testboard.testdir)
        self._setupdir_testboard(Testboard)
        if 'IV' in self.currenttest:
            self.log <<" %s: send testdir to %s: %s"%(self.agente_name, self.client_name, Testboard.testdir)
            self.sclient.send(self.highVoltageSubscription,":PROG:IV:TESTDIR %s\n"%Testboard.testdir)
            self.open_testboard(Testboard)

    def powercycle(self):
        self.currenttest='powercycle'
        for Testboard in self.Testboards:
            self._prepare_testboard(Testboard)
        self.execute_test()
        while not self.check_finished():
            sleep(1)
        self.cleanup_test()

    def execute_test(self):
        if not self.active:
            return False
        self.pending = True
        # Runs a test
        self.sclient.clearPackets(self.subscription)
        if self.currenttest.lower().startswith('iv') or self.currenttest.lower().startswith('cycle'):
            self.pending = False
            return True
        elif not self.currenttest == 'powercycle':
            pass
        else:
            self.log << 'Powercycling Testboards'
        for Testboard in self.Testboards:
            self._execute_testboard(Testboard)
        return True    

            #Here we need the Errorstream of the watchdog:

            #packet = self.sclient.getFirstPacket(coolingBoxSubscription)
            #if not packet.isEmpty() and not "pong" in packet.data.lower():
            #    data = packet.data
            #    Time,coms,typ,msg = decode(data)[:4]
            #    if coms[0].find('STAT')==0 and typ == 'a' and 'ERROR' in msg[0].upper():
            #        self.log.warning('jumo has error!')
            #        self.log.warning('\t--> I will abort the tests...')
            #        self.log.printn()
            #        for Testboard in self.Testboards:
            #            self.sclient.send(self.subscription,':prog:TB%s:kill\n'%Testboard.slot)
            #            self.log.warning('\t Killing psi46 at Testboard %s'%Testboard.slot)
            #            index=[Testboard.slot==int(coms[1][2]) for Testboard in self.Testboards].index(True)
            #            Testboard.failed()
            #            Testboard.busy=False


    def _execute_testboard(self,Testboard): 
        Testboard.busy=True
        self.sclient.send(self.subscription,':prog:TB%s:start %s,%s,commander_%s\n'%(Testboard.slot,self.Directories['testdefDir']+'/'+ self.currenttest,Testboard.testdir,self.currenttest))
        if not self.currenttest == 'powercycle':
            self.log << 'psi46 at Testboard %s is now started'%Testboard.slot

    def cleanup_test(self):
        # Run after a test has executed
        if not self.active:
            return True
        if 'IV' in self.currenttest:
            for Testboard in self.Testboards:
                if Testboard.slot == self.activeTestboard:
                    self.close_testboard(Testboard)
                    Testboard.numerator += 1 
        elif not self.currenttest == 'powercycle':  
            for Testboard in self.Testboards:
                Testboard.numerator += 1
        else:
            for Testboard in self.Testboards:
                self._deldir(Testboard)
        return True

    def final_test_cleanup(self):
        # Run after a test has executed
        self.powercycle()
        if not self.active:
            return True
        return True

    def check_finished(self):
        if not self.active or not self.pending:
            return True
        packet = self.sclient.getFirstPacket(self.subscription)
        if not packet.isEmpty() and not "pong" in packet.data.lower():
            data = packet.data
            Time,coms,typ,msg = decode(data)[:4]
            if coms[0].find('STAT')==0 and coms[1].find('TB')==0 and typ == 'a' and msg=='test:finished':
                try:
                    index=[Testboard.slot==int(coms[1][2]) for Testboard in self.Testboards].index(True)
                    self.Testboards[index].busy=False
                except:
                    self.log<<"Couldn't find TB with slot %s"%coms[1][2]
            if coms[0][0:4] == 'STAT' and coms[1][0:2] == 'TB' and typ == 'a' and msg=='test:failed':
                try:
                    index=[Testboard.slot==int(coms[1][2]) for Testboard in self.Testboards].index(True)
                except:
                    self.log<<"Couldn't find TB with slot %s"%coms[1][2]
                    index =-1
                if self.currenttest == 'powercycle' and index !=-1:
                    sleep(1)
                    raise Exception('Could not open Testboard at %s.'%Testboard.slot)
                self.Testboards[index].busy=False
        self.pending = any([Testboard.busy for Testboard in self.Testboards])
        self.log<<[Testboard.busy for Testboard in self.Testboards]
        return not self.pending

    def _setupdir_testboard(self,Testboard):
        if not self.currenttest == 'powercycle':
            self.log << 'Setting up the directory:'
            self.log << '\t- %s'%Testboard.testdir
            self.log << '\t  with Parameters from %s' % self.test.parent.parameter_dir[Testboard.slot]
        #copy directory
        try:
            self.test.parameter_dir[Testboard.slot] = Testboard.testdir
            copytree(self.test.parent.parameter_dir[Testboard.slot], Testboard.testdir)
            self._setup_configfiles(Testboard)
        except IOError as e:
            self.log.warning("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except OSError as e:
            self.log.warning("OS error({0}): {1}".format(e.errno, e.strerror))
            raise

    def _setup_configfiles(self, Testboard):
        """ Changes config files in the already copied test directory according to test definitions
            from elComandante's init file. """
        # Change testboard name
        self._config_file_content_substitute(Testboard.testdir + "/configParameters.dat", {"testboardName":Testboard.address})

        # Get test specific config parameters (if available)
        params = ()
        try:
            params = self.init.items("Test " + self.test.testname)
        except:
            return

        for par in params:
            file = par[0]
            # Check for valid keys that represent config files
            if "testParameters" in file or "dacParameters" in file or "configParameters" in file:
                pass
            elif "tbmParameters" in file or "tbParameters" in file:
                pass
            else:
                continue

            encoded_keys = par[1].split(",")
            keys = {}
            for key in encoded_keys:
                key = key.split("=", 2)
                if len(key) != 2:
                    continue
                keys[key[0]] = key[1]
            if len(file) < 4 or file[-4:] != ".dat":
                file += ".dat"
            self._config_file_content_substitute(Testboard.testdir + "/" + file, keys)

    def _config_file_content_substitute(self, filename, keys):
        """ Substitutes configuration lines in a file according to the dictionary "keys" """
        # Open the file for substitution
        try:
            f = open(filename, "r")
            lines = f.readlines()
            f.close()
        except:
            self.log.warning("Error reading from parameter file " + filename + ".")
            raise

        try:
            # Backup the original file
            f = open(filename + ".original", "w")
            f.write("".join(lines))
            f.close()
        except:
            self.log.warning("Error making a backup file of " + filename + ". Skipped.")

        # Define the fields within the file
        fields = 2
        keyfield = 0
        datafield = 1
        if "dacParameters" in filename or "tbmParameters" in filename or "tbParameters" in filename:
            fields = 3
            keyfield = 1
            datafield = 2

        # iterate over all lines
        for i in range(len(lines)):
            line = lines[i].strip()
            if len(line) == 0 or line[0] == '-' or line[0] == '#':
                continue
            line = line.split(None, fields - 1)
            if len(line) != fields:
                continue
            # check whether this line matches a key
            if not line[keyfield] in keys:
                continue
            line[datafield] = keys[line[keyfield]]
            lines[i] = " ".join(line)
            lines[i] += '\n'

        try:
            # Write the new file
            f = open(filename, "w")
            f.write("".join(lines))
            f.close()
        except:
            self.log.warning("Error saving parameters in " + filename + ".")
            raise

    def _deldir(self,Testboard):
        try:
            rmtree(Testboard.testdir)
        except:
            self.log.warning("Couldn't remove directory")
            pass

    def open_testboard(self,Testboard):
        self.sclient.clearPackets(self.subscription)
        self.log << "%s: Opening Testboard %s ..." % (self.agente_name, Testboard.slot)
        self.sclient.send(self.subscription,':prog:TB%s:open %s, %s\n'%(Testboard.slot,Testboard.testdir,Testboard.currenttest)) 
    
    def close_testboard(self,Testboard):
        self.log << "%s: Closing Testboard %s ..." % (self.agente_name, Testboard.slot)
        self.sclient.send(self.subscription,':prog:TB%s:close %s\n'%(Testboard.slot,Testboard.testdir))
