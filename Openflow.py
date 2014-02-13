from pox.core import core
from pox.lib.addresses import EthAddr
import openflow.libopenflow_01 as of
import pox.openflow.nicira as nx
import threading
import time
import pox.lib.packet as pkt

from Schema import Schema
from LatencyMeasurment import LatencyMeasurment


#pass in connection

class Openflow(threading.Thread):
    
    #should have way to send match objects to a switch thats just come online    
    matches = []
    
    def __init__(self, schemas):
        #core.openflow.addListeners(self) # never ever have this line uncommented.
        core.openflow.addListenerByName("PacketIn",self.handlePacketIn)
        core.openflow.addListenerByName("PortStatus",self.showPortStatus)
        self.schemas = schemas
        threading.Thread.__init__(self)
        """for s in self.schemas.schemas:
            print "adding request..."
            print s.openflow.items()
            print "---------------------"
            self.addNewRequest(s)"""

    def run(self):
        while True:
            self.measureLatency("1","2")
        

    def handlePacketIn(self,event):
        packet = event.parsed
        ether = packet.find('ethernet')
        if ether and ether.type==0001: 
            finish = time.time()
            tTotal = finish - self.timeStamp 
            latency = tTotal -(self.timeS1/2) - (self.timeS1/2)
            print "switch one "+ str(self.timeS1/2)
            print "switch two "+ str(self.timeS2/2)
            print "total " + str(tTotal)
            print "latency between switch one and switch two is: "+str(latency)
             
            
        """
        packetRequest = Schema()
        packetRequest.fromPacket(packet)

        when packet is received, go through all requests to see who's interested
        for originalRequest in self.schemas.schemas:

            if originalRequest.equals(packetRequest):
                print "application "+str(originalRequest.application)+" wanted "+str(originalRequest.openflow.items())
                print "found: " + str(packetRequest.openflow.items())
                print "\n\n"
        """
            

    

    def _handle_ConnectionUp(self,event):
        print "connection up"
        #Tutorial(event.connection)
        event.connection.send(nx.nx_packet_in_format())
        
        for m in self.matches:
            print "sending "
            self.sendMatch(m,event.connection) 

    def _handle_ConnectionDown(self,event):
        pass

    def createMatch(self,request):
        #loop over dictionary, use switch statement
        match = of.ofp_match()
        for attribute,value in request.openflow.items():
            if attribute=="IngressPort":
                match.in_port=value
            elif attribute=="EthernetSource":
                match.dl_src=value
            elif attribute=="EthernetDestination":
                match.dl_dst=value
            elif attribute=="EthernetType":
                match.dl_type=value
            elif attribute=="VLANpriority":
                match.dl_vlan_pop=value
            elif attribute=="IPSourceAddress":
                match.nw_src=value
            elif attribute=="IPDestinationAddress":
                match.nw_dst=value
            elif attribute=="IPprotocol":
                match.nw_proto
            elif attribute=="IPToS":
                match.nw_tos=value
            elif attribute=="sourcePort":
                match.tp_src=value
            elif attribute=="destinationPort":
                match.tp_dst=value
            elif attribute=="VLANID":
                match.dl_vlan=value
        return match

    
        


    def sendMatch(self,match,connection):
        message = of.ofp_flow_mod()
        message.match = match
        
        connection.send(message)
        
    def addNewRequest(self,request):
        print "adding request " + str(request.openflow.items())
        
        match = self.createMatch(request)
        self.matches.append(match)  
        
        
        
   
        
        
    """sometimes the second switch has a much lower time. maybe cache concerns
       
       eventually have a list of links that openflow needs to measure, based on schemas
       """    
    def measureLatency(self,switchOne, switchTwo):  
        self.TimeTotal = 0 #time between controller, s1, s2
        time.sleep(5)
        s1 = None
        s2 = None
        """go through the list of connected switches, mapping between s1 and the dpid trim the input
        
        for core.connections print strpid"""
        for switch in core.openflow.connections:
            #print "Switch " + str(switch.dpid)
            if switchOne.strip() == str(switch.dpid):
                s1 = switch
            if switchTwo.strip() == str(switch.dpid):
                s2 = switch
                
        print switchOne+" is "+str(s1)
        print switchTwo+" is "+str(s2)
        
        measureSwitchOne = LatencyMeasurment(s1)
        measureSwitchTwo = LatencyMeasurment(s2)
        print "Round trip time to switch one: "+str(measureSwitchOne.roundTripTime)
        print "Round trip time to switch two: "+str(measureSwitchTwo.roundTripTime)
        self.timeS1 = measureSwitchOne.roundTripTime
        self.timeS2 = measureSwitchTwo.roundTripTime
        
        
        
        """send flow mod to switch, put timestamp in ethernet packet, and choose the right port that goes to s2"""
        
        match = of.ofp_match()
        match.dl_type= 0001
        self.sendLatencyFlowMod(s1)
        time.sleep(1)
        self.sendLatencyEthernetPacket(2,s1) #get port number from mac address
        
        
        
        " to get the port, use mac table?"
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
        #timeStamp = time.time()
        #ether.payload = timeStamp
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
       


    



    
          




        
