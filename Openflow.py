from pox.core import core

from pox.lib.addresses import EthAddr
import openflow.libopenflow_01 as of
import pox.openflow.nicira as nx

import time
import pox.lib.packet as pkt
import pox.lib.util

from Schema import Schema
from LatencyMeasurement import LatencyMeasurement
from Switch import Switch

import threading



class Openflow(threading.Thread):

    
    def __init__(self, schemas):
        #core.openflow.addListeners(self) # never ever have this line uncommented.
        #core.openflow.addListenerByName("PacketIn",self.handlePacketIn)
        core.openflow.addListenerByName("PortStatus",self.showPortStatus)
        core.openflow.addListenerByName("ConnectionUp",self.handleConnectionUp)
        core.openflow.addListenerByName("ConnectionDown",self.handleConnectionDown)
        self.schemas = schemas.schemas
        self.switches = {}
        self.results = {}
        self.links = []
        threading.Thread.__init__(self)
        self.getLinks()
         
    
    def run(self):
        while True:
             for s  in self.schemas: 
                 if s.latency:
                     time.sleep(3) # so different packets are not mixed up
                     self.processLatencyRequest(s)
                 
            
            
    def getLinks(self):
        for s in self.schemas:
            if s.latency:
                self.links.append(s.latency[0])
        


    def handleConnectionUp(self,event):
        self.switches[event.connection.dpid] =  event.connection
        

    def handleConnectionDown(self,event):
        self.switches.pop(event.connection.dpid)              
        
             
    
    def processLatencyRequest(self,schema):
        switches = schema.latency[0]
        linkLatency = LatencyMeasurement(switches[0],switches[1],self.switches)

        while linkLatency.latency==0: #wait for all the packets to be sent and handled
            pass
        latency = linkLatency.latency
        
        threshold = schema.latency[1]
        if(schema.latency[2]==0):   
                if(latency * 1000) <= threshold:
                        self.results[(switches[0],switches[1])] = latency
        else:
                if(latency*1000) >= threshold:
                    self.results[(switches[0],switches[1])] = latency
        
        
        
    
      
        
    def showPortStatus (self, event):
        if event.added:
            action = "added"
        elif event.deleted:
            action = "removed"
        else:
            action = "modified"
        print "Port %s on Switch %s has been %s." % (event.port, event.dpid, action)
       


    



    
          




        
