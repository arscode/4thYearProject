from pox.core import core

from pox.lib.addresses import EthAddr
import openflow.libopenflow_01 as of
import pox.openflow.nicira as nx
import threading
import time
import pox.lib.packet as pkt
import pox.lib.util

from Schema import Schema
from LatencyMeasurment import LatencyMeasurment
from Switch import Switch



class Openflow(threading.Thread):

    
    def __init__(self, schemas):
        #core.openflow.addListeners(self) # never ever have this line uncommented.
        core.openflow.addListenerByName("PacketIn",self.handlePacketIn)
        core.openflow.addListenerByName("PortStatus",self.showPortStatus)
        core.openflow.addListenerByName("ConnectionUp",self.handleConnectionUp)
        core.openflow.addListenerByName("ConnectionDown",self.handleConnectionDown)
        self.schemas = schemas.schemas
        self.switches = {}
        self.currentSwitches = []
        self.currentLatency = 0
        self.latencyType = 0
        self.results = {}
        self.links = []
        threading.Thread.__init__(self)
        self.getLinks()
        
        
        coreOne = ("00-00-00-04-01-01",{"00-00-00-00-02-01":1,"00-00-00-01-02-01":2,"00-00-00-02-02-01":3,"00-00-00-03-02-1":4})
        coreTwo = ("00-00-00-04-01-02",{"00-00-00-00-02-01":1,"00-00-00-01-02-01":2,"00-00-00-02-02-01":3,"00-00-00-03-02-1":4})
        coreThree = ("00-00-00-04-02-01",{"00-00-00-00-03-01":1,"00-00-00-01-03-01":2,"00-00-00-02-03-01":3,"00-00-00-03-03-1":4})
        coreFour = ("00-00-00-04-02-02",{"00-00-00-00-03-01":1,"00-00-00-01-03-01":2,"00-00-00-02-03-01":3,"00-00-00-03-03-1":4})
        
        aggregateOne = ("00-00-00-00-02-01",{"00-00-00-04-01-01":1,"00-00-00-00-00-01":2,"00-00-00-04-01-02":3,"00-00-00-00-01-01":4})
        aggregateTwo = ("00-00-00-00-03-01",{"00-00-00-04-02-01":1,"00-00-00-00-00-01":2,"00-00-00-04-02-02":3,"00-00-00-00-01-01":4})
        aggregateThree = ("00-00-00-01-02-01",{"00-00-00-04-01-01":1,"00-00-00-01-00-01":2,"00-00-00-04-01-02":3,"00-00-00-01-01-01":4})
        aggregateFour = ("00-00-00-01-03-01",{"00-00-00-04-02-01":1,"00-00-00-01-00-01":2,"00-00-00-04-02-02":3,"00-00-00-01-01-01":4})
        aggregateFive = ("00-00-00-02-02-01",{"00-00-00-04-01-01":1,"00-00-00-02-00-01":2,"00-00-00-04-01-02":3,"00-00-00-02-01-01":4})
        aggregateSix = ("00-00-00-02-03-01",{"00-00-00-04-02-01":1,"00-00-00-02-00-01":2,"00-00-00-04-02-02":3,"00-00-00-02-01-01":4})
        aggregateSeven = ("00-00-00-03-02-01",{"00-00-00-04-01-01":1,"00-00-00-03-00-01":2,"00-00-00-04-01-02":3,"00-00-00-03-01-01":4})
        aggregateEight = ("00-00-00-03-03-01",{"00-00-00-04-02-01":1,"00-00-00-03-00-01":2,"00-00-00-04-02-02":3,"00-00-00-03-01-01":4})
   
        self.switchMap = [coreOne,coreTwo,coreThree,coreFour,aggregateOne,aggregateTwo,aggregateThree,aggregateFour,aggregateFive,aggregateSix,aggregateSeven,aggregateEight]
    
    
    def run(self):
        while True:
             for s  in self.schemas: #"""need to give packets time to be sent. limitation."""
                 if s.latency:
                     time.sleep(1)
                     switches = s.latency[0]
                     self.measureLatency(switches[0],switches[1])
                     self.currentLatency = s.latency[1]
                     self.latencyType = s.latency[2]
                 
            #self.measureLatency("00-00-00-00-02-01","")
            
            
    def getLinks(self):
        for s in self.schemas:
            if s.latency:
                self.links.append(s.latency[0])
        

    def handlePacketIn(self,event):
        packet = event.parsed
        ether = packet.find('ethernet')
        if ether and ether.type==0001: 
            finish = time.time()
            tTotal = finish - self.timeStamp 
            latency = tTotal -((self.timeS1/2) + (self.timeS2/2))
          
            """this is one way, not rtt, like ping is"""
            #print "latency threshold", str(self.currentLatency)
            #print "actual latency", str(latency*1000)
           
            """0 for less, 1 for more"""
            if(self.latencyType==0):   
                if(latency * 1000) <= self.currentLatency:
                        self.results[self.currentSwitches] = latency
            else:
                if(latency*1000) >= self.currentLatency:
                    self.results[self.currentSwitches] = latency

    def handleConnectionUp(self,event):
        self.switches[event.connection.dpid] =  event.connection
        

    def handleConnectionDown(self,event):
        self.switches.pop(event.connection.dpid)              
        
    """sometimes the second switch has a much lower time. maybe cache concerns
       use list of switches to find out what port to use
       eventually have a list of links that openflow needs to measure, based on schemas
       
       have a dictionary of tuple of two switches as key, time as value
       put this dictionary as shared memory
       """    
    def measureLatency(self,switchOne, switchTwo):  
        self.TimeTotal = 0 #time between controller, s1, s2
        self.currentSwitches = (switchOne,switchTwo)
        time.sleep(5)
        s1 = None
        s2 = None
        for switchDPID in self.switches:
            if switchOne.strip() == pox.lib.util.dpid_to_str(switchDPID):
                s1 = self.switches[switchDPID]
            if switchTwo.strip() == pox.lib.util.dpid_to_str(switchDPID):
                s2 = self.switches[switchDPID]
                
        """s1 and s2 is a switch object"""
        measureSwitchOne = LatencyMeasurment(s1)
        measureSwitchTwo = LatencyMeasurment(s2)
       # print "Round trip time to switch one: "+str(measureSwitchOne.roundTripTime)
        #print "Round trip time to switch two: "+str(measureSwitchTwo.roundTripTime)
        self.timeS1 = measureSwitchOne.roundTripTime
        self.timeS2 = measureSwitchTwo.roundTripTime
        
        
        
        """send flow mod to switch, put timestamp in ethernet packet, and choose the right port that goes to s2"""
        
        match = of.ofp_match()
        match.dl_type= 0001
        self.sendLatencyFlowMod(s1)
        time.sleep(1)
        s1MAC = (str(s1)[1:-3]).strip()
        s2MAC = (str(s2)[1:-3]).strip()
        port = None
        print  s1MAC +" wants to find the port number for "+s2MAC
       
        for s in self.switchMap:
            if (s[0]).strip() == s1MAC:
                port = s[1][s2MAC]
        self.sendLatencyEthernetPacket(port,s1)
        
        
    """maybe put specific links as well, in the packet, so can measure a lot at once"""
    def sendLatencyEthernetPacket(self,outPort,switch):
        ether = pkt.ethernet()
        #effective_ethertype
        ether.type = 0001 #arbitary type, taken from paper
        ether.dst = EthAddr("ff:ff:ff:ff:ff:ff")
        ether.src = EthAddr("01:02:03:04:05:06")
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=outPort)
        msg.actions.append(action)
        self.timeStamp= time.time()
    
        msg.data = ether
        print "sending ethernet packet"
        switch.send(msg)
        "put time stamp in etherpacket. this is working, just need to add payload"
        
    def sendLatencyFlowMod(self,switch):
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0001
        print "sending flow..."
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
        switch.send(msg)
        
        
    def showPortStatus (self, event):
        if event.added:
            action = "added"
        elif event.deleted:
            action = "removed"
        else:
            action = "modified"
        print "Port %s on Switch %s has been %s." % (event.port, event.dpid, action)
       


    



    
          




        
