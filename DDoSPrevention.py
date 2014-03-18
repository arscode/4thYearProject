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
        self.colours = {"RED":"\033[1m\033[31m","WHITE":"\033[1m\033[37m","GREEN":"\033[1m\033[32m","END":"\033[0m"}


        self.blockedIps = {}
        self.pushMonitoringFlow()
        self.pushThreshold(threshold)


   
       
        
        
        
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
    
    """need a way to check that ip is already blocked. so not blocking it over and over"""
    def run(self):
        while True:
            time.sleep(1)
            
            for ip in self.blockedIps.keys():
                timeStamp = self.blockedIps[ip]
                print ip,timeStamp
                if (time.time()-timeStamp) >(120): #two minutes
                    self.blockedIps.pop(ip) #take it out of current list of ips being blocked
                    self.unblock(ip)
           
            for ip in self.checkThreshold():
                self.block(ip) 
           
        
        
    #in check threshold, call block if its not already in self.ips...and update self.ip
    """get list of ips that are above the threshold
        add them to a list of ips currently being blocked
        and return a list of new naughty ips to block"""
    def checkThreshold(self):
        
        url = "/events/json?maxEvents=10"
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

                    """check that a sourceIP was returned, and its not already being blocked"""
                    if sourceIP and (sourceIP,destIP) not in self.blockedIps:
                        if destIP != None:
                            print self.colours["RED"]+"detected new attack from "+sourceIP+" to "+destIP+self.colours["END"]
                        else:
                            print self.colours["RED"]+"detected new attack from "+sourceIP+self.colours["END"]

                        newips.append((sourceIP,destIP))
                        self.blockedIps[(sourceIP,destIP)] = time.time()

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
        if the event was over two minutes ago, forget it. 
         otherwise the same events are picked up again    """

        timeStamp = recentAttacks[0]["lastUpdate"]
        if (timeStamp>=120000):
            return None,None
 
   
        """if icmp no broadcast address so only one entry
        if len(recentAttacks)<2:
            print attackerInfo
            return None,None
            """
        """if the timestamp is older than a minute, disregard the old event"""

        ipaddresses = (recentAttacks[0]["key"]).split(',')
        """depending on type of attack, there might not be a dest ip addr"""
        if len(ipaddresses)==1:
            sourceIP = ipaddresses[0]
            destIP = None
        else:
            sourceIP = ipaddresses[0]
            destIP = ipaddresses[1]

        if sourceIP != "0.0.0.0" and sourceIP != "255.255.255.255":
            #print recentAttacks
            return sourceIP,destIP
        return None,None

    
    
    def block(self,ip):
        msg = of.ofp_flow_mod()
        action = of.ofp_action_output(port=of.OFPP_NONE)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = IPAddr(ip[0]) 
        #match.nw_dst = IPAddr(ip[1])
        msg.match = match
        print self.colours["GREEN"]+"blocking ",ip[0]+self.colours["END"]
        """blocking too much. check the stages -think about what should happen
            maybe problem is its blocking host ips. see if can fake ips. """
        for connection in core.openflow.connections:
            connection.send(msg)
    

    """could also just set the idle timeout """   
    def unblock(self,ip):
        msg = of.ofp_packet_out()
        action = of.ofp_action_output(port=of.OFPP_NONE)
        msg.actions.append(action)
        match = of.ofp_match()
        match.nw_src = IPAddr(ip[0])
        #match.nw_dst = IPAddr(ip[1])
        msg.command = of.OFPFC_DELETE
        msg.match = match
        print self.colours["WHITE"]+"unblocking ",ip[0]+self.colours["END"]
        for connection in core.openflow.connections:
            connection.send(msg)
        
        
        
    


   
   
   