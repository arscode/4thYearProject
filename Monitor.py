from pox.core import core
import openflow.libopenflow_01 as of
import pox.openflow.nicira as nx

from Request import Request

#pass in connection

class Monitor(object):
	
	#should have way to send match objects to a switch thats just come online	
	matches = []
	switches = []
	

	def __init__(self, requests):
		core.openflow.addListeners(self) # need this to handle events
		core.openflow.addListenerByName("PacketIn",self.handleStuff)
		for r in requests.requests:
			self.addNewRequest(r)	



	def handleStuff(self,event):
		
		print "packet in---------------"
		packet = event.parsed
		#request = request()
		#request.fromPacket(packet)
		#print request.openflow.items()
		#get reference to request store, turn into request, see if any match
		#write equals object for request
		
	

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
		#message.actions.append(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
		connection.send(message)
		
	def addNewRequest(self,request):
		print "adding request " + request.application
		match = self.createMatch(request)
		self.matches.append(match)	


	




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
        print "dst in dictionary"
	print self.mac_to_port
    	self.resend_packet(packet_in, self.mac_to_port[packet.dst])

      # Once you have the above working, try pushing a flow entry
      # instead of resending the packet (comment out the above and
      # uncomment and complete the below.)

        log.debug("Installing flow...")
      # Maybe the log statement should have source/destination/port?

      #msg = of.ofp_flow_mod()
      #
      ## Set fields to match received packet
      #msg.match = of.ofp_match.from_packet(packet)
      #
      #< Set other fields of flow_mod (timeouts? buffer_id?) >
      #
      #< Add an output action, and send -- similar to resend_packet() >

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



      
	
	       
		



	
	      




		
