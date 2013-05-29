#!/usr/bin/python2
import sys
sys.path.insert(1, "../")
from myutils import sClient, decode, printer, is_float
from threading import Thread
import subprocess
import time
import argparse
import keithleyInterface
import os
import serial
import signal
from time import sleep
ON = 1
OFF = 0
End = False
Logger = printer()
IVLogger = printer()
Logger.set_name("KeithleyLog")
IVLogger.set_name("ivLog")
#sweep parameters TODO anpassen
startValue = -100
stopValue = -200
stepValue = 15
nSweeps = 1
delay =.1
maxSweepTries=1
doingSweep = False

defSerialPort = '/dev/tty.usbserial-FTG7MJTY'
serialPort = defSerialPort

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--device", dest="serialPort",
                       help="serial Port address e.g. /dev/ttyF0",
                       default=defSerialPort)
parser.add_argument("-dir","--directory", dest='dataDir',
                       help='directory where LogFilse is Stored',
                       default='.')
parser.add_argument('-ts','--timestamp', dest='timestamp',
                       help='Timestamp for creation of file',
                       default=0)

args = parser.parse_args()
serialPort= args.serialPort
try:
    os.stat(args.dataDir)
except:
    os.mkdir(args.dataDir)
#Setup Logger 
Logger.timestamp = float(args.timestamp)
Logger.set_logfile('%s/Keithley.log'%(args.dataDir))
Logger.set_prefix('')
#default testDir, should be set (by elComandante)  when doing IV curve
testDir = '%s'%(args.dataDir)
IVLogger.set_logfile('%s/IV.log'%(args.dataDir))
IVLogger.set_prefix('')
IVLogger.timestamp = float(args.timestamp)
IVLogger.disable_print()
if not os.access(serialPort,os.R_OK):
    Logger.warning('serialPort \'%s\' is not accessible'%serialPort)
    sys.exit()
    raise SystemExit
Logger<<'SerialPort: %s'% serialPort

def handler(signum, frame):
    Logger << 'Close Connection'
    client.closeConnection()
    Logger << 'Signal handler called with signal %s'%signum
    try:
        keithley.setOutput(OFF)
    except:
        pass
    if client.isClosed == True:
        Logger << 'client connection closed: kill all'
        End=True
        Logger << 'End: %s'%End
    
signal.signal(signal.SIGINT, handler)


serverZiel = '127.0.0.1'
serverPort = 12334
aboName = '/keithley'
IVAbo = '/keithley/IV'
voltageAbo = '/keithley/voltage'
currentAbo = '/keithley/current'
resistanceAbo='/keithley/resistance'
client = sClient(serverZiel,serverPort,"keithleyClient")
client.subscribe(aboName)
client.send(aboName,'Connecting Keithley Client with Subsystem\n')
keithley=keithleyInterface.keithleyInterface(serialPort)
keithley.setOutput(OFF)
#Logger << 'status:%s'%keithley.getOutputStatus()

def readCurrentIV():
    if keithley.getOutputStatus():
        data= keithley.getAnswerForQuery(':READ?',69).split(' ')
        timestamp = time.time()
        if len(data)==5:
            if is_float(data[0]) and is_float(data[1]) and is_float(data[2]):
                voltage = float(data[0])
                current = float(data[1])
                resistance = float(data[2])
                #Logger << '%s: %s V - %s A'%(timestamp,data[0],data[1])
                IVLogger << '%s: %s V - %s A'%(timestamp,data[0],data[1])
                client.send(voltageAbo,'%s\n'%voltage)
                client.send(currentAbo,'%s\n'%current)
                client.send(resistanceAbo,'%s\n'%resistance)
        else:
            #Logger << ' could somehow not read data correctly: %s'%data
            pass
    else:
        pass
        #Logger << 'output is off'
        
def sweep():
    global doingSweep
    global testDir
    doingSweep = True
    outputStatus = keithley.getOutputStatus()
    client.send(aboName,':MSG! Start with Linear Sweep from %sV to %sV in %sV steps\n'%(startValue,stopValue,stepValue))
    Logger << "TestDirectory is: %s"%testDir
    ntries = 0
    while True:
        retVal = keithley.doLinearSweep(startValue, stopValue, stepValue, nSweeps, delay)
#        Logger << 'keithley RetVal: %s'%retVal
        ntries+=1
        if retVal!=0 or ntries>=maxSweepTries:
            Logger << 'exit while loop'
            break
        voltage = keithley.getLastVoltage()
        msg='Keithley Tripped %s of %s times @ %s\n'%(ntries,maxSweepTries,voltage)
        Logger << msg
        client.send(aboName,msg)
        client.send(IVAbo,msg) 
    client.send(aboName,'Results of Linear Sweep:\n')
    client.send(IVAbo,'Results Start:\n')
    client.sendData(voltageAbo,'Sweep Data\n')
    client.sendData(currentAbo,'Sweep Data\n')
    client.sendData(resistanceAbo,'Sweep Data\n')
    client.send(aboName,':PROG:IV! RESULTS\n')
    npoint = 0
    nPoints = len(keithley.measurments)
    ivCurveLogger = printer()
    ivCurveLogger.set_name("ivCurveLogger")
    ivCurveLogger.disable_print()
#    ivCurveLogger.timestamp = float(args.timestamp)
    ivCurveLogger.set_prefix('')
    ivCurveLogger.set_logfile('%s/ivCurve.log'%testDir)
    ivCurveLogger << '#timestamp\tvoltage(V)\tcurrent(A)'
    while len(keithley.measurments)>0:
        npoint +=1
        measurement = keithley.measurments.popleft()
        measurement[0]=int(measurement[0])
        timestamp = measurement[0]
        voltage = float(measurement[1])
        current = float(measurement[2])
#        resistance = float(measurement[3])
        client.sendData(aboName,':IV! %s/%s '%(npoint,nPoints) +" ".join(map(str, measurement[:3]))+'\n')
        client.sendData(IVAbo," ".join(map(str, measurement[:3]))+'\n')
        strA = '%d %+8.3f'%(timestamp,voltage)
        strA = strA.strip('\n')
        strA += '\n'
        try:
            client.sendData(voltageAbo,strA)
        except:
            Logger.warning("Couldn't send '%s'"%strA)
        strA = '%d %+11.4e'%(timestamp,current)
        strA = strA.strip('\n')
        strA += '\n'
        try:
            client.sendData(currentAbo,'%d %+11.4e\n'%(timestamp,current))
        except:
            Logger.warning("Couldn't send '%s'"%strA)
        try:
            ivCurveLogger << '%d\t%+8.3f\t%+11.4e'%(timestamp,voltage,current)
        except:
            pass
#        IVLogger << '%s\t%s\t%s'%(timestamp,voltage,current)
#        client.sendData(resistanceAbo,'%s %s\n'%(timestamp,resistance))
    client.send(IVAbo,'Results End\n')
    client.send(aboName,':PROG:IV! FINISHED\n')
    client.send(voltageAbo,'Sweep Data Done\n')
    client.send(currentAbo,'Sweep Data Done\n')
    client.send(resistanceAbo,'Sweep Data Done\n')
    del ivCurveLogger
    sleep(1)
    keithley.initKeithley()
    keithley.setOutput(outputStatus)
    doingSweep =  False



############################################################################
############################################################################
############################################################################

def printHelp():
    data = '\n************************************************************************\n'
    data +=  'This is the Help for the python keithley client, part of elComandante\n'
    data +=' You can use following SCPI like commands: \n'
    data +='\t:HELP                \tto show this Help\n'
    data +='\t:OUTPut ON/OFF       \tto switch the Output of the Keithley ON/OFF\n'
    data +='\t:OUTPut?             \tto query the current status of the Output of the Keithley\n'
    data +='\t:PROG:IV MEASURE     \tto make an IV Curve for the current device\n'
    data +='\t:PROG:IV:TESTDIR   XX\tSetPArentDir to Save the IV Data\n'
    data +='\t:PROG:IV:START     XX\tto make an IV Curve for the current device\n'
    data +='\t:PROG:IV:STOP      XX\tto make an IV Curve for the current device\n'
    data +='\t:PROG:IV:STEP      XX\tto make an IV Curve for the current device\n'
    data +='\t:PROG:IV:DELay     XX\tto make an IV Curve for the current device\n'
    data +='\t:PROG:IV:MAXTRIPS  XX\tto set maximum tries if keithley is tripping\n'
    data +='\t:PROG:RESISTANCE   XX\tto enable/disable 4-Wire Resistance Measurement\n'
    data += '************************************************************************\n'
    Logger << data
    client.sendData(aboName,data)
    
def  analyseIV(coms,typ,msg):
    global startValue
    global stopValue
    global delay
    global stepValue
    global maxSwepTries
    global nSweeps
    global testDir
#    Logger <<'analyse :IV'
    if len(coms)==0:
        if msg.lower().find('meas')>=0 and typ=='c':
            outMsg= ':MSG! Do Sweep from %.2f V to %.2f'%(startValue,stopValue)
            outMsg+=' in steps of %.2fV with a delay of %.f\n'%(stepValue,delay)
            outMsg+='\tTestDirectory is "%s"\n'%testDir
            Logger << outMsg
            client.send(aboName,outMsg)
            sweep()
        elif typ!='a':
            Logger << 'error'
            printHelp()
    elif len(coms)==1:
#        Logger << 'iv len >0'
        outMsg = 'not Valid Input'
        if coms[0].lower().find('testdir')>=0:
            if typ =='c':
#                Logger << '%s: "%s"'%(coms[0],msg)
                testDir = msg
                try:
                    os.stat(testDir)
#                    Logger << 'checked Directory'
                except:
                    outMsg = ':IV:TESTDIR! %s: directory does not exist. Error!'%testDir
                else:
                    outMsg = ':IV:TESTDIR! %s'%testDir

        if coms[0].find('START')>=0:
            if typ =='c' and is_float(msg):
                startValue=float(msg)
#                Logger << 'prog-iv-start=%s'%msg
            elif typ =='q':
#                Logger << 'prog-iv-start?'
                pass
            outMsg = ':PROG:IV:START! %s'%startValue
        elif coms[0].find('STOP')>=0:
            if typ =='c'and is_float(msg):
                stopValue = float(msg)
#                Logger << 'prog-iv-stop=%s'%msg
            elif typ =='q':
#                Logger << 'prog-iv-stop?'
                pass
            outMsg = ':PROG:IV:STOP! %s'%stopValue
        elif coms[0].find('STEP')>=0:
            if typ =='c'and is_float(msg):
                stepValue=float(msg)
#                Logger << 'prog-iv-step=%s'%msg
            elif typ =='q':
#                Logger << 'prog-iv-step?'
                pass
            outMsg = ':PROG:IV:STEP! %s'%stepValue
        elif coms[0].find('DEL')>=0:           
            if typ =='c'and is_float(msg):
                delay=float(msg)
#                Logger << 'prog-iv-delay=%s'%msg
            elif typ =='q':
#                Logger << 'prog-iv-delay?'
                Logger
            outMsg = ':PROG:IV:DELAY! %s'%delay
        elif coms[0].find('MAXTRIPS')>=0:           
            if typ =='c' and is_float(msg):
                maxSweepTries=float(msg)
#                Logger << 'prog-iv-trip=%s'%msg
            elif typ =='q':
#                Logger << 'prog-iv-trip?'
                pass
            outMsg = ':PROG:IV:TRIP! %s'%delay
        Logger << outMsg
        outMsg+='\n'
        client.send(aboName,outMsg)
    elif typ != 'a':
#        Logger << 'error prog iv len to long'
        printHelp()
    pass
        
def analyseProg(coms,typ,msg):
#    Logger << 'analyse :PROG'
#    Logger << coms
    if coms[0].find('IV')>=0:
        analyseIV(coms[1:],typ,msg)
        pass
    elif coms[0].find('RESISTANCE')>=0 and typ =='c':
        if msg in ['ON','TRUE','1']:
            keithley.initFourWireResistensMeasurement()
        elif msg in ['OFF','FALSE','0']:
            keithley.initKeithley()
    elif coms[0].find('EXIT')>=0 and typ =='c':
#        Logger << 'end program'
        client.closeConnection();
    else:
        printHelp()
    pass

def analyseOutp(coms,typ,msg): #pretty much ok
    #Logger << 'analyse Output'
    if len(coms)>0 and  typ != 'a':
#        Logger << 'not valid command: %s %s %s '%(coms, typ, msg)
        printHelp()
    else:
        if typ=='q':
            Logger << 'Query for output status'
            status = keithley.getOutputStatus()
            outMsg = ':OUTP! '
            outMsg+= 'ON' if status else 'OFF'
            outMsg+='\n'
#            Logger << outMsg
            client.send(aboName,outMsg)
        elif typ=='c':
            if msg in ['1','ON','True']:
                keithley.setOutput(ON)
            elif msg in ['0','OFF','False']:
                keithley.setOutput(OFF)
            elif  typ != 'a':
                Logger << 'message of :OUTP not valid: %s, valid messages are \'ON\',\'OFF\''%msg
                printHelp()
        elif  typ != 'a':
            Logger << 'this a non valid typ'
            printHelp()
    pass

def analysePacket(coms,typ,msg):
    if coms[0].find('PROG')>=0:
        if len(coms[1:])>0:
            analyseProg(coms[1:],typ,msg)
        elif typ != 'a':
            Logger << 'not valid packet: %s'%coms
            printHelp()
        pass
    elif coms[0].find('OUTP')>=0:
        analyseOutp(coms[1:],typ,msg)
        pass
    elif coms[0].find('HELP')>=0 and typ != 'a':
        printHelp()
    elif coms[0]=='K':
        command = ":".join(map(str, coms[1:]))+' '+msg
        Logger << 'send command to keithley: '
        keithley.write(command)
    elif coms[0].lower().startswith('exit') and typ != 'a':
        client.closeConnection()
    else:
        Logger << 'not Valid Packet %s'%coms
        


############################################################################
############################################################################
############################################################################
#RECEIVE COMMANDS:

sleep(0.5)
counter = 0 
while client.anzahl_threads > 0 and End == False and client.isClosed == False: 
    
    counter +=1
    sleep(.5)
    packet = client.getFirstPacket(aboName)
    
    if not packet.isEmpty():

        #Logger << 'got Packet: %s'%packet.Print()
        data = packet.data
        timeStamp,coms,typ,msg,command = decode(data)
        # 'T:',timeStamp, 'Comand:',command
        #Logger << '%s: %s, %s, %s'%(timeStamp,len(coms),typ,msg)
        dataOut = '%s\n'%packet.Print()
        if command.find(':DOSWEEP')!=-1:
            sweep()
        if len(coms)>0:
            analysePacket(coms,typ,msg)
        else:
            keithley.write(command)
            client.send(aboName,dataOut)
        #string retVal = keithley.setOutput(ON)
    else:
       # Logger << client.getNumberOfPackets(),' packets are left in queue'
       pass
    if counter%10 == 0:      
        if not doingSweep:
            readCurrentIV()
    pass   
        
        

client.send(aboName,':prog:stat! exit\n')    
Logger << 'exiting...'
client.closeConnection()

#END
while client.anzahl_threads > 0:
    sleep(1)
    pass            
Logger << 'ciao!'

