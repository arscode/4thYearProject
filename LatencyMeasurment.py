

"""because I want to encapsulate all the latency measurement stuff
   I have to do use a dedicated class for it
   cant just have one method, because I need to handle the stats recieved event
   measure latency for one single switch """
import time
import openflow.libopenflow_01 as of
from pox.core import core

   
   
class LatencyMeasurment():
    
    def __init__(self,switch):
        self.switch = switch
        self.startTime = 0
        self.endTime = 0
        core.openflow.addListenerByName("FlowStatsReceived",self.handleStatsReply)
        
        self.measureLatency()
        
        
        
    def sendStatsRequest(self):
        self.startTime = time.time() 
        self.switch.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
        
    
    
    def measureLatency(self):
        self.sendStatsRequest()
        """wait for the reply"""
        while (self.endTime == 0): 
            pass
        self.roundTripTime = self.endTime - self.startTime
        
        
        
        
        
    def handleStatsReply(self,event):
        #should be the only stats reply, but check anyway
        if event.connection == self.switch:
            self.endTime = time.time()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            