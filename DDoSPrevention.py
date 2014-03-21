"""takes in a threshold, defines a flow to monitor it, defines threshold, periodically polls
   if threshold exceeded, time stamp and block ip. later on, unblock ips again"""

import threading
import json
import httplib
import time
import openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.addresses import IPAddr
from pox.lib.revent import EventHalt


class DDoSPrevention(threading.Thread):
    
    
    def __init__(self,threshold):
        threading.Thread.__init__(self)
        self.colours = {"RED":"\033[1m\033[31m","WHITE":"\033[1m\033[37m","GREEN":"\033[1m\033[32m","END":"\033[0m"}
        """priority one so it overrides controller and changing path"""
        core.openflow.addListenerByName("PacketIn",self.dropPacket,priority=100000)

        self.hosts = ["10.0.0.2","10.0.0.3","10.0.1.2","10.0.1.3","10.1.0.2","10.1.0.3","10.1.1.2","10.1.1.3","10.2.0.2","10.2.0.3","10.2.1.2","10.2.1.3","10.3.0.2","10.3.0.3","10.3.1.2","10.3.1.3"]

        self.blockedIps = {}
        self.pushMonitoringFlow()
        self.pushThreshold(threshold)


   
    """this stops riplpox from routing the packet, effectively dropping it
    it stops the packet from going to a host, but it still goes to the controller
    and still would take up a bit of bandwith in the network        
    exactly how mac blocker works, how it meant to be done?                         """   
    def dropPacket(self,event):
        #packet = event.parsed
        ip = event.parsed.find('ipv4')
        if ip and str(ip.srcip) in self.blockedIps:
            return EventHalt



        
        
    #
        
    def pushMonitoringFlow(self):
        url = "/flow/ddos/json"
        payload = "{keys:'ipsource,ipdestination,icmpcode', value:'bytes'}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    
    
    def pushThreshold(self,threshold):
        url = "/threshold/ddos/json"
        payload = "{metric:'ddos',value:"+str(threshold)+"}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    """ """
    def run(self):
        while True:
            time.sleep(1)
            
            for ip in self.blockedIps.keys():
                timeStamp = self.blockedIps[ip]
                
                if (time.time()-timeStamp) >(300): #two minutes
                    self.blockedIps.pop(ip) #take it out of current list of ips being blocked
                    self.unblock(ip)

            for ip in self.checkThreshold():
                self.block(ip) 
           
        

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
                if event["metric"] == "ddos":   
                    agent = event["agent"]
                    sourceIP,destIP = self.getDetailedFlowInfo(agent)
                   

                     
                    """check it hasn't caught a response instead of the outgoing connection"""
                    if sourceIP in self.hosts:
                        if destIP not in self.blockedIps:
                            print self.colours["RED"]+"detected new attack from "+destIP+" to "+sourceIP+self.colours["END"]
                            newips.append(destIP)
                            self.blockedIps[destIP] = time.time()


                    elif destIP in self.hosts:
                        if sourceIP not in self.blockedIps:
                            print self.colours["RED"]+"detected new attack from "+sourceIP+" to "+destIP+self.colours["END"]
                            newips.append(sourceIP)
                            self.blockedIps[sourceIP] = time.time()

                    
                            

                        
        return newips


    """uses the agent ip addr to get more detailed flow info
       lots of crude parsing here....something to work on """
    def getDetailedFlowInfo(self,agent):
        url = "/metric/"+str(agent)+"/ddos/json"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("GET",url," ")
        response = connection.getresponse()
        attackerInfo = json.loads(response.read())
     

        if not "topKeys" in attackerInfo[0]:
            #rint attackerInfo
            return None,None

       

        recentAttacks = attackerInfo[0]["topKeys"]
        
        """the timestamp is how many millseconds ago the event was generated
        if the event was over five minutes ago, forget it. 
         otherwise the same events are picked up again    """
        timeStamp = recentAttacks[0]["lastUpdate"]
        if (timeStamp>=300000):
            return None,None
 

        ipaddresses = (recentAttacks[0]["key"]).split(',')

        """depending on type of attack, there might not be a dest ip addr"""
        if len(ipaddresses)==1:
            sourceIP = ipaddresses[0]
            destIP = None
            print "only one"
        else:
            sourceIP = ipaddresses[0]
            destIP = ipaddresses[1]

        if sourceIP != "0.0.0.0" and sourceIP != "255.255.255.255":
            #print recentAttacks
            return sourceIP,destIP
        return None,None

    
    
    def block(self,ip):
        match = of.ofp_match()
        match.nw_src = IPAddr(ip) 
      
        print self.colours["GREEN"]+"blocking ",ip+self.colours["END"]
        msg2 = of.ofp_flow_mod(command=of.OFPFC_ADD,actions=[],match=match)
        for connection in core.openflow.connections:
            connection.send(msg2)
    

    """could also just set the hard timeout """   
    def unblock(self,ip):
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=of.OFPP_CONTROLLER)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = IPAddr(ip)
        #match.nw_dst = IPAddr(ip[1])
        msg.command = of.OFPFC_DELETE
        msg.match = match
        print self.colours["WHITE"]+"unblocking ",ip+self.colours["END"]
        for connection in core.openflow.connections:
            connection.send(msg)
        
        
        
    


   
   
   