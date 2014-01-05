#from home.james.pox.pox.core import core
#import home.james.pox.pox.openflow.libopenflow_01



class Monitor(object):
	
	#should have way to send match objects to a switch thats just come online	
	switches= []

	def __init__(self, requests):
		core.openflow.addListeners(self) # need this to handle events
		core.openflow.addListenerByName("PacketIn",handleEvent)
		for r in requests:
			self.addNewRequest(r)	

	def _handle_ConnectionUp(self,event):
		self.switches.add(event.connection)

	def _handle_ConnectionDown(self,event):
		self.switches.remove(event.connection)

	def createMatch(request):
		#loop over dictionary, use switch statement
		match = of.ofp_match()
		for attribute,value in enumerate(request.openflow()):
			if attribute=="IngressPort":
				match.in_port=value
			elif attribute=="EthernetSource":
				match.dl_src=value
			elif attrribute=="EthernetDestination":
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


	def sendMatch(match,connection):
		message = ofp_flow_mod()
		message.match = match
		message.buffer_id = None
		message.idle_timeout = idle_timeout
		message.hard_timeout = hard_timeout
		message.actions.append(of.ofp_action_output(port=OFPP_CONTROLLER))
		connection.send(message)
		
	def addNewRequest(request):
		print "adding request " + request.application
		match = self.createMatch(request)
		for c in self.switches:
			sendMatch(match,c)
						

	def handleEvent(self, event):
		pass


		
