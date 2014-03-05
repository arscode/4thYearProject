"""takes in a threshold, defines a flow to monitor it, defines threshold, periodically polls
   if threshold exceeded, time stamp and block ip. later on, unblock ips again"""

import threading
import httplib
import time
import openflow.libopenflow_01 as of
from pox.core import core


class DDoSPrevention(threading.Thread):
    
    
    def __init__(self,threshold):
        self.pushMonitoringFlow()
        self.pushThreshold(threshold)
        self.monitor()
        self.ips = {}
        
        
        
        
    def pushMonitoringFlow(self):
        url = "/flow/ddos/json"
        payload = "{keys:'ipsource,ipdestination', value:'frames'}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    
    
    def pushThreshold(self,threshold):
        url = "/threshold/ddos/json"
        payload = "{metric:'ddos',value:"+threshold+"}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    
    def monitor(self):
        time.sleep(1)
        for ip,time in self.ips.iteritems():
            if (time.time()-time) >(120): #two minutes
                ips.remove(ip) #take it out of current list of ips being blocked
                self.unblock(ip)
                
        self.checkThreshold()
        for ip in ips:
            self.block(ip)
        
        
    
    
    def checkThreshold(self):
        url = "/events/json?eventID=4&timeout=60"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("GET",url," ")
        response = connection.getresponse()
        events = json.loads(response.read())
        
        if len(events)> 0:
            for event in events[0]["topKeys"]:
                key = event["key"]
                print key
                if key not in self.ips:
                    self.ips[key] = time.time()
        return ips
    
    
    def block(self,ip):
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=OFPP_NONE)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = ip #make sure ip is correct here
        msg.match = match
        for connection in core.openflow.connections:
            connection.send(msg)
    
    
    """might have to be more complicated, and handle packetIn in my code. see if riplpox will
        do it for me first."""
    def unblock(self,ip):
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=OFPP_CONTROLLER)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = ip #make sure ip is correct here
        msg.match = match
        for connection in core.openflow.connections:
            connection.send(msg)
        
        
        
    


   
   
   