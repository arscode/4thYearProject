


from lxml import etree
from pox.core import core
import pox.openflow.libopenflow_01 as of

class Request:
	openflow = {}
	application = None
	openflowAttributes = ('IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID')


	def __init__(self):
		pass
	
		


	def fromFile(self,f):
		schema=None
		with open("FlowSchema.xml") as s:
			schema = etree.parse(s)
		schema = etree.XMLSchema(schema)
		parser = etree.XMLParser(schema = schema)
		tree = etree.parse(f,parser)

		for attribute in self.openflowAttributes:
			path = '/request/openflow/'+attribute
			element = tree.xpath(path)
			if element:
				self.openflow[attribute] = (element[0].text).strip()
		self.application = (tree.xpath("application")[0].text).strip()


	def fromPacket(self, packet):
		ip = packet.find('ipv4')
		if ip:
			self.openflow["IPSourceAddress"]=ip.srcip
			self.openflow["IPDestinationAddress"]=ip.dstip
			self.openflow["IPToS"]=ip.tos
			self.openflow["IPprotocol"]=ip.protocol
		
		ether = packet.find('ethernet')
		if ether:
			self.openflow["EthernetSource"]=ether.src
			self.openflow["EthernetDestination"]=ether.dst
			self.openflow["EthernetType"]=ether.type
		tcp = packet.find('tcp')
		if tcp:
			self.openflow["sourcePort"] = tcp.srcport
			self.openflow["destinationPort"] = tcp.dstport
		udp = packet.find('udp')
		if udp:	
			self.openflow["sourcePort"] = tcp.srcport
			self.openflow["destinationPort"] = tcp.dstport


		
