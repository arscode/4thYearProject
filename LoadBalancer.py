
import time
import openflow.libopenflow_01 as of
from pox.core import core
import pox.lib.util
import pox.lib.packet as pkt
from pox.lib.addresses import EthAddr
import threading

"""set up flow for each switch. use that to determine how much traffic is flowing through them
use this to work out how much each switch has compared to other swithes on same path
two parts. 
two parts. need a dictionary that holds switch info dicti, and code that goes through it. 

what switches to monitor? 



use openflow to see how much traffic is being sent over each switch. then, can 

dictionary of switchs and total bytes
periodically get switch stats. use spanning tree routing. when a switch is overloaded, change the routing

"""

class LoadBalancer(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
        core.openflow.addListenerByName("FlowStatsReceived",handleFlowStats)



    def run(self):
    	while True:
    	    time.sleep(10)
            self.getSwitchStats()



	def getSwitchStats(self):
		for switch in core.openflow.connections:
			switch.send(of.ofp_stats_request(body=of.ofp_flow_stats_request())))


    def handleFlowStats(self,event):
    	totalBytes = 0
    	for f in event.stats:
    		if f.match.tp_dst == 80 or f.match.tp_src == 80:
    			totalBytes += f.byte_count

    	print "total bytes flowing through ",event

