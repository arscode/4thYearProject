




#put request into dictionary, also update list of stuff to monitor

#when events happen, run through dictionary and see what programs want to be infinformed


from pox.core import core
import pox.openflow.libopenflow_01 as of
from Monitor import Monitor
from Request import Request
import os
import re



class RequestStore:
	requests = []

	def __init__(self,xmlFiles):
		for xmlFile in xmlFiles:
			request = Request()
			request.fromFile(xmlFile)
			self.requests += [request]
				
	def printRequests(self):
		for r in self.requests:
			print r.application
			print  r.openflow.items()
	



#put in requeststore?
def getFiles():
	allFiles = os.listdir(os.getcwd())
	print "current working directory is "+os.getcwd()
	xmlFiles = []
	xmlPattern= re.compile('^.*\.(xml)$')
	for fileName in allFiles:
		m = re.match(xmlPattern,fileName)
		if m and fileName != "FlowSchema.xml":
			xmlFiles += [m.group(0)]
	print xmlFiles
	return xmlFiles


def start_switch(event):
	Tutorial(event.connection)

			
		
def launch():	
	allRequests = RequestStore(getFiles())
	allRequests.printRequests()
	m = Monitor(allRequests)

	#core.openflow.addListenerByName("ConnectionUp", start_switch)


class Switch(object):
	mac_to_port = {}

	def __init__ (self, connection):
	      print "initialising switch"
    	      self.connection = connection
	      print connection
              connection.addListeners(self) 
	

	
	def _handle_PacketIn (self, event):
	      print "packet in "
   	      packet = event.parsed # This is the parsed packet data.
	      print "MAC addresses are " + str(packet.dst)[:2] +", "+ str(packet.src)

      

              if not packet.parsed:
                  log.warning("Ignoring incomplete packet")
                  return
	      print "good"
              packet_in = event.ofp # The actual ofp_packet_in message.
              
              self.act_like_switch(packet, packet_in)


  	def resend_packet (self, packet_in, out_port):
  	       msg = of.ofp_packet_out()
    	       msg.data = packet_in
               action = of.ofp_action_output(port = out_port)
               msg.actions.append(action)
               self.connection.send(msg)


	def act_like_switch (self, packet, packet_in):
	       print "packet from " +str(packet_in.in_port)+" and " +str(packet.src)
	       print "packet going to " + str(packet.dst)
               self.mac_to_port[packet.src] = packet_in.in_port
	       if packet.dst not in self.mac_to_port:
	       	   self.resend_packet(packet_in, of.OFPP_ALL)

	       else:
	           self.resend_packet(packet_in, self.mac_to_port[packet.dst])






class Tutorial (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}


  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)




  def act_like_switch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """



    # Here's some psuedocode to start you off implementing a learning
    # switch.  You'll need to rewrite it as real Python code.

    # Learn the port for the source MAC
    self.mac_to_port[packet.src] = packet_in.in_port

    if packet.dst in self.mac_to_port:
	print self.mac_to_port[packet.dst]
     
    	#self.resend_packet(packet_in, self.mac_to_port[packet.dst])



    

        msg = of.ofp_flow_mod()
      #
      ## Set fields to match received packet
        msg.match = of.ofp_match.from_packet(packet)
      #
      #< Set other fields of flow_mod (timeouts? buffer_id?) >
      #
	msg.data = packet_in
        msg.actions.append(of.ofp_action_output(port=self.mac_to_port[packet.dst]))
	self.connection.send(msg)

    else:
      # Flood the packet out everything but the input port
      # This part looks familiar, right?
        self.resend_packet(packet_in, of.OFPP_ALL)



  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.

    # Comment out the following line and uncomment the one after
    # when starting the exercise.
   # self.act_like_hub(packet, packet_in)
    self.act_like_switch(packet, packet_in)












			


