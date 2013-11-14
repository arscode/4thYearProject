
"""get reference to switch from connection
   install flow that matches web packets
   redirect web packets to a different host
   use wireshark/tcp to verify this
"""

"""install flow for web, take host to forward it to as a parameter"""


from pox.core import core
from pox.lib.util import dpid_to_str
import pox.openflow.libopenflow_01 as of

class Logger(object):
    def __init__(self):
        core.openflow.addListeners(self) 
        
    def _handle_ConnectionUp(self,event):
        print "Switch %s is up.",dpid_to_str(event.dpid)

    def _handle_ConnectionDown(self,event):
        print "Switch %s is down.",dpid_to_str(event.dpid)

    def _handle_PortStatus(self,event):
        if event.added:
            action = "added"
        if event.deleted:
            action = "removed"
        else:
            action = "modified"
        print "Port %s on switch %s has been %s.",event.port,dpid_to_str(event.dpid),action


def webFlow(event):
    """first define match rules"""
    msg = of.ofp_flow_mod()
    webMatch = of.ofp_match(tp_src=80)
    msg.match = webMatch
    """if its web, send packet to controller"""
    print "Pushing web flow to "+dpid_to_str(event.dpid)
    msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    event.connection.send(msg)
    """packet gets sent to controller. need a listener function for this, packetIn"""




def checkTraffic(event): 
    print "Checking Traffic"
    tcp_bytes = 0
    for flow in event.stats:
        if flow.match.tp_dst==80 or flow.match.tp_src==80:
            tcp_bytes += flow.byte_count
    print "bytes: "
    print tcp_bytes
    redirectTraffic()
    if tcp_bytes>30000: #iperf maxes out at about 36k 
        redirectTraffic()


def redirectTraffic():
    msg = of.ofp_flow_mod()
    tcpMatch = of.ofp_match(tp_src=80,tp_dst=80)
    msg.match = tcpMatch
    print "redirecting flow to switch 2"
    msg.actions.append(of.ofp_action_output(port=2))
    core.openflow.getConnection(1).send(msg)

def sendStats(event):
    if event.parsed.find('tcp'):
        print "sending stats"
        event.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
   

"""Write a class that turns a switch into a learning switch. Write a listener that creates a learning switch from a connectionUp."""

def launch():
    """everytime a connection is established to a switch, push a flow onto it""" 
    core.openflow.addListenerByName("ConnectionUp",webFlow)
    core.openflow.addListenerByName("FlowStatsReceived",checkTraffic)
    core.openflow.addListenerByName("PacketIn",sendStats)


