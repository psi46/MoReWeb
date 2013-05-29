'''
    subsystem Client for PYTHON
    by Felix Bachmair and Philipp Eller 
    at IPP, ETH Zurich
    in March 2012
    
    this clients looks for new packets in the background via a thread
    the packets are saved in  a queue. One can get the oldest packet via
    getFirstPacket(aboName)
    
    The Subsystem protocol is developed at RWTH Aachen by Dennis Terhorst
    and Jochen Steinmann
    This protocol is intended to be used for the subsystem service,
    providing a network based data aquisition scheme and is used for
    client-server communication. It uses IP/UDP packets to provide
    sensor data and control messages to the networked system components.
    It is intended to be a light-weight protocol which can be implemented
    on many differernt platforms, including very limited environments
    like micro-controllers or embedded systems.
    For more information see subserver documentation in repository
    
    TODO:
        create new init function which just takes a name and looks for the 
         "real" subserver address and port by its own

'''

from time import sleep
from time import time
import socket
import struct
import signal, os
import thread
import threading
import select
 
lock = thread.allocate_lock() 

                            
class packet_t:
    PKT_MANAGEMENT = 0
    PKT_DATA = 1
    PKT_SUBSCRIBE = 2
    PKT_UNSUBSCRIBE = 3
    PKT_SUPPLY = 4
    PKT_UNSUPPLY = 5
    PKT_CLIENTTERM = 6
    PKT_SERVERTERM = 7
    PKT_SETDATA = 8
    PKT_DEFAULTTYPE = PKT_DATA
    
    def __init__(self,ziel,port):
        self.type = self.PKT_DEFAULTTYPE
        self.ziel = ziel
        self.port = port
        self.aboName =''
        self.data=''
    def extractData(self,rawData):
        self.type,self.leng = struct.unpack('hh',rawData[:4])
        self.type = socket.ntohs(self.type)
        self.leng = socket.ntohs(self.leng)
        self.aboName = rawData[4:4+self.leng-1].strip()
        self.aboName=self.aboName.strip()
        self.data = rawData[4+self.leng:].strip()
        self.data=self.data.strip()
    def isEmpty(self):   
        if self.aboName =='' and self.data=='' and self.type == self.PKT_DEFAULTTYPE:
            return True
        if self.data=='' and self.type==self.PKT_DATA:
            return True
        else:
            return False
    def Print(self):
        return '\"%s %s %s\"'%(self.type, self.aboName, self.data)

    def createPackage(self):
        aboname=self.aboName+ '\0';
        type = (socket.htons(self.type))
        leng = (socket.htons(len(aboname)))
        fmt = 'hh%ss%ss'%(len(aboname),len(self.data))
        output = struct.pack(fmt,int(type),int(leng),aboname,self.data)
        return output
###############################################################        
class sClient:
    sleepTime = 0.1 
    MAXLENGTH = 2047
    SUBSERVER_ENVNAME = "SUBSERVER"
    SUBSERVER_DEFAULT_ADDR = "127.0.0.1"
    SUBSERVER_DEFAULT_PORT = 12334
    def __init__(self,Ziel,port,name):
        self.sendTimeStamp = True
        self.ziel = Ziel
        self.port = port
        self.udp_sock = socket.socket( socket.AF_INET,  socket.SOCK_DGRAM )
        self.udp_sock.setblocking(0)
        self.udp_sock.settimeout(0.1)
        self.receivedPackets = []
        #print name
        self.clientName = name
        self.setID( name ) 
        self.isClosed = False 
        self.anzahl_threads = 0
        self.thread_gestartet = False
        self.receiveThread()  
        self.logAbo='/log'
        self.send(self.logAbo,'Started new Client %s\n'%name)         
    def setID(self,name):
        if name != self.clientName:
            self.send(self.logAbo,'change client name from %s to %s\n'%(self.clientName,name))
        self.clientName = name
        idPacket = packet_t(self.ziel,self.port)
        idPacket.type = idPacket.PKT_MANAGEMENT
        idPacket.aboName=''
        idPacket.data = 'setid %s\0'%name  
        self.sendPacket(idPacket) 
    def subscribe(self,aboName):
        aboPacket = packet_t(self.ziel,self.port)
        aboPacket.type = aboPacket.PKT_SUBSCRIBE
        aboPacket.aboName = aboName
        self.sendPacket(aboPacket)
    def unsubscribe(self,aboName):
        aboPacket = packet_t(self.ziel,self.port)
        aboPacket.type = aboPacket.PKT_UNSUBSCRIBE
        aboPacket.aboName = aboName
        self.sendPacket(aboPacket)              
    def sendPacket(self,packet):
        self.udp_sock.sendto( packet.createPackage(),(packet.ziel,packet.port))          
    def unsupply(self,aboName):
        aboPacket = packet_t(self.ziel,self.port)
        aboPacket.type = aboPacket.PKT_UNSUPPLY
        aboPacket.aboName = aboName
        self.sendPacket(aboPacket)
    def supply(self,aboName):
        aboPacket = packet_t(self.ziel,self.port)
        aboPacket.type = aboPacket.PKT_SUPPLY
        aboPacket.aboName = aboName
        self.sendPacket(aboPacket)
    def sendData(self,aboName,data):
        dataPacket = packet_t(self.ziel,self.port)
        dataPacket.type = dataPacket.PKT_DATA
        dataPacket.aboName = aboName
        dataPacket.data =data
        self.sendPacket(dataPacket)    
    def sendTimStampData(self,aboName,data):
        self.sendTSData(aboName,data)
    def sendTSData(self,aboName,data):
        currentTime = time()
        TSData = '%s %s'%(long(time()),data)
        self.sendData(aboName,TSData)
    def send(self,aboName,data):
        if self.sendTimeStamp:
            self.sendTSData(aboName,data)
        else:
            self.sendData(aboName,data)
    def echoToPing(self,aboName):
        self.sendTSData(aboName,":Pong! %s\n"%self.clientName)
    def checkSubscription(self,aboName):
        #print 'ping? %s'%aboName
        nTested = 0;
        retVal = False
        while nTested<3 and retVal == False:
            nTested += 1
            self.sendTSData(aboName,":Ping?\n")
            sleep(1);
            sleep(self.sleepTime)
            for pkt in self.receivedPackets:
                if 'pong' in pkt.data.lower():
                    self.receivedPackets.pop(self.receivedPackets.index(pkt))
                    retVal = True
        return retVal
    def receivePacket(self):
        try:    
            data, addr =self.udp_sock.recvfrom( self.MAXLENGTH ) 
            newPacket = packet_t(self.ziel,self.port)
            newPacket.extractData(data)
            newPacket.Print()
            if "ping" in newPacket.data.lower():
                self.echoToPing(newPacket.aboName)
            else:
                self.receivedPackets.append(newPacket)
                #print 'received ', len(self.receivedPackets),'Packets'   
        except socket.timeout as e:
            #print 'TIMEOUT: %s'%e
            pass 
        except socket.error as e:
#            print '%s'%(e)
#            print '%s'%type(e)
            errno = e.errno
            msg = ' '
            print '\nACHTUNG::::: Exception in receivePacket: %s: %s, %s\n\n'%(errno,msg,e)
            self.sendTSData(self.logAbo,'Exception in receivePacket: %s: %s\n'%(errno,msg))
            if errno == 4:
                print 'receive ends'
                self.closeConnection()   
            elif errno == 11:
                pass
            else: 
                raise
    def receivePackets(self):
        lock.acquire()
        self.anzahl_threads += 1 
        self.thread_gestartet = True 
        lock.release() 
        while self.isClosed == False:
            self.receivePacket()
            sleep(self.sleepTime)
        self.closeConnection()                
        lock.acquire() 
        self.anzahl_threads -= 1 
        lock.release()     
    def receiveThread(self):
#        thread.start_new_thread(self.receivePackets,())
        threading.Thread(target=self.receivePackets, args=()).start()
        while not self.thread_gestartet and self.anzahl_threads == 0: 
            pass 
    def closeConnection(self):
        closePacket =packet_t(self.ziel,self.port)
        closePacket.type = closePacket.PKT_CLIENTTERM
        closePacket.aboName = ''
        self.send(self.logAbo,'closing client %s\n'%self.clientName)
        self.sendPacket(closePacket)
        self.isClosed = True
        #print 'Closed Connection of Client',self.clientName
    def getFirstPacket(self,aboName):
        for packet in self.receivedPackets:
            if packet.aboName == aboName:
                return self.receivedPackets.pop(self.receivedPackets.index(packet))
                break
            if self.anzahl_threads == 0:
                break
        return packet_t(self.ziel,self.port)
    def getNumberOfPackets(self):
        length = len(self.receivedPackets)
        return length
    
    def clearPackets(self,aboName):
        for packet in self.receivedPackets:
            if packet.aboName == aboName:
                self.receivedPackets.pop(self.receivedPackets.index(packet))
            if self.anzahl_threads == 0:
                break        

