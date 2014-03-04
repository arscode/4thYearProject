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
             for s  in self.schemas: 
                 if s.latency:
                     time.sleep(1) # so different packets are not mixed up
                     self.processLatencyRequest(s)
                 
            #self.measureLatency("00-00-00-00-02-01","")
            
            
    def getLinks(self):
        for s in self.schemas:
            if s.latency:
                self.links.append(s.latency[0])
        


    def handleConnectionUp(self,event):
        print "switch up"
        self.switches[event.connection.dpid] =  event.connection
        

    def handleConnectionDown(self,event):
        self.switches.pop(event.connection.dpid)              
        
             
    
    def processLatencyRequest(self,schema):
        switches = schema[0]
        linkLatency = LatencyMeasurement(switches[0],switches[1])
        while linkLatency.latency==0:
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
       


    



    
          




        
