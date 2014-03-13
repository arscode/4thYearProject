"""takes in a threshold, defines a flow to monitor it, defines threshold, periodically polls
   if threshold exceeded, time stamp and block ip. later on, unblock ips again"""

import threading
import json
import httplib
import time
import openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.addresses import IPAddr


class DDoSPrevention(threading.Thread):
    
    
    def __init__(self,threshold):
        threading.Thread.__init__(self)
        self.ips = {}
        self.pushMonitoringFlow()
        self.pushThreshold(threshold)
        print "ips are ",self.ips
       
        
        
        
        
        
    def pushMonitoringFlow(self):
        url = "/flow/ddos/json"
        payload = "{keys:'ipsource,ipdestination', value:'frames'}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    
    
    def pushThreshold(self,threshold):
        url = "/threshold/ddos/json"
        payload = "{metric:'ddos',value:"+str(threshold)+"}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    
    def run(self):
        while True:
            time.sleep(1)
            print "monitoring for ddos"
            for ip,timeStamp in self.ips.iteritems():
               
                if (time.time()-timeStamp) >(120): #two minutes
                    ips.remove(ip) #take it out of current list of ips being blocked
                    self.unblock(ip)
             
            for ip in self.checkThreshold():
                self.block(ip)
            
        
        
    #check for event id, so make sure not adding duplicates
    """get list of ips that are above the threshold
        add them to a list of ips currently being blocked
        and return a list of new naughty ips to block"""
    def checkThreshold(self):
        
        url = "/events/json"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("GET",url," ")
        response = connection.getresponse()
        events = json.loads(response.read())
        
        newips = []
        if len(events)> 0:
            for event in events:
                print event
                if event["metric"] == "ddos":
                    ipaddr = event["agent"]
                    print ipaddr
                    newips.append(ipaddr)
                    if ipaddr not in self.ips: #why not just override?
                        self.ips[ipaddr] = time.time()

        return newips
    
    
    def block(self,ip):
        msg = of.ofp_flow_mod()
        action = of.ofp_action_output(port=of.OFPP_NONE)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = IPAddr(ip) #make sure ip is correct here
        msg.match = match
        print msg
        for connection in core.openflow.connections:
            connection.send(msg)
    
    
    """might have to be more complicated, and handle packetIn in my code. see if riplpox will
        do it for me first."""
    def unblock(self,ip):
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=of.OFPP_CONTROLLER)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = ip #make sure ip is correct here
        msg.match = match
        for connection in core.openflow.connections:
            connection.send(msg)
        
        
        
    


   
   
   